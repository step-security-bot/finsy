"""Implements a DemoNet class for running Mininet tests in a container."""

import argparse
import asyncio
import contextlib
import json
import os
import re
import socket
import time
from dataclasses import KW_ONLY, asdict, dataclass, field
from ipaddress import IPv4Network, IPv6Network
from pathlib import Path
from types import TracebackType
from typing import Any, Sequence

from shellous import Command, Runner, sh
from shellous.prompt import Prompt

from finsy import MACAddress

try:
    import pygraphviz as pgv  # type: ignore
except ImportError:
    pgv = None

# pyright: reportUnknownMemberType=false

IPV4_BASE = IPv4Network("10.0.0.0/8")
IPV6_BASE = IPv6Network("fc00::/64")


class Directive:
    "Marker superclass for all Demo configuration directives."


@dataclass
class CopyFile:
    source: Path
    dest: str


@dataclass
class Image(Directive):
    name: str
    _: KW_ONLY
    kind: str = field(default="image", init=False)
    files: Sequence[CopyFile] = field(default_factory=list)


@dataclass
class Switch(Directive):
    name: str
    _: KW_ONLY
    kind: str = field(default="switch", init=False)
    params: dict[str, Any] = field(default_factory=dict)
    commands: list[str] = field(default_factory=list)


@dataclass
class Host(Directive):
    name: str
    switch: str = ""
    _: KW_ONLY
    kind: str = field(default="host", init=False)
    ifname: str = "eth0"
    mac: str = "auto"
    ipv4: str = "auto"
    ipv4_gw: str = ""
    ipv6: str = ""
    ipv6_gw: str = ""
    ipv6_linklocal: bool = False
    static_arp: dict[str, str] = field(default_factory=dict)
    disable_offload: Sequence[str] = ("tx", "rx", "sg")
    commands: list[str] = field(default_factory=list)

    # These fields are "assigned" when configuration is initially processed.
    assigned_switch_port: int = field(default=0, init=False)
    assigned_mac: str = field(default="", init=False)
    assigned_ipv4: str = field(default="", init=False)
    assigned_ipv6: str = field(default="", init=False)

    def init(self, host_id: int) -> None:
        "Derive MAC and IP addresses when necessary."
        if self.mac == "auto":
            self.assigned_mac = str(MACAddress(host_id))
        else:
            self.assigned_mac = self.mac

        if self.ipv4 == "auto":
            self.assigned_ipv4 = f"{IPV4_BASE[host_id]}/{IPV4_BASE.prefixlen}"
        else:
            self.assigned_ipv4 = self.ipv4

        if self.ipv6 == "auto":
            self.assigned_ipv6 = f"{IPV6_BASE[host_id]}/{IPV6_BASE.prefixlen}"
        else:
            self.assigned_ipv6 = self.ipv6


@dataclass
class Link(Directive):
    start: str
    end: str
    _: KW_ONLY
    kind: str = field(default="link", init=False)
    style: str = ""
    commands: list[str] = field(default_factory=list)
    assigned_start_port: int = field(default=0, init=False)
    assigned_end_port: int = field(default=0, init=False)


@dataclass
class Pod(Directive):
    name: str
    _: KW_ONLY
    kind: str = field(default="pod", init=False)
    images: Sequence[Image] = field(default_factory=list)
    publish: Sequence[int] = field(default_factory=list)


@dataclass
class Bridge(Directive):
    name: str
    _: KW_ONLY
    kind: str = field(default="bridge", init=False)
    mac: str = ""
    ipv4: str = ""
    commands: list[str] = field(default_factory=list)


class Config:
    "Manages a DemoNet configuration."

    items: Sequence[Directive]

    def __init__(
        self,
        items: Sequence[Directive],
    ):
        self.items = items
        self._scan_directives()

    def image(self) -> Image:
        "Return the configured docker image, or the default image if none found."
        images = [item for item in self.items if isinstance(item, Image)]
        if len(images) > 1:
            raise ValueError("There should only be one Image config.")
        if not images:
            return Image("docker.io/opennetworking/p4mn")
        return images[0]

    def switch_count(self) -> int:
        "Return the number of switches in the config."
        return sum(1 for item in self.items if isinstance(item, Switch))

    def draw(self, filename: str):
        "Draw the network to `filename`."
        graph = self.to_graph()
        graph.layout()
        graph.draw(filename)

    def _scan_directives(self):
        """Scan the directives and fill in necessary details.

        This method modifies unset fields in the configuration. It is safe to do
        this more than once; this is an idempotent operation.

        TODO: Make directives read-only and do copy-on-write for changes.
        """
        port_db = _ConfigPortDB()
        host_id = 1

        for item in self.items:
            match item:
                case Switch():
                    port_db.add_switch(item.name)
                case Host():
                    item.init(host_id)
                    host_id += 1
                    if item.switch:
                        item.assigned_switch_port = port_db.next_port(item.switch)
                case Link():
                    if item.start in port_db:
                        item.assigned_start_port = port_db.next_port(item.start)
                    if item.end in port_db:
                        item.assigned_end_port = port_db.next_port(item.end)
                case _:
                    pass

            if isinstance(item, (Switch, Host, Link, Bridge)):
                # Replace "$DEMONET_IP" in "commands".
                item.commands = [
                    s.replace("$DEMONET_IP", _LOCAL_IP) for s in item.commands
                ]

    def to_json(self, **kwds: Any) -> str:
        return json.dumps(self.items, default=Config._json_default, **kwds)

    @staticmethod
    def _json_default(obj: object):
        if isinstance(obj, Path):
            return str(obj)

        try:
            return asdict(obj)  # pyright: ignore[reportGeneralTypeIssues]
        except TypeError as ex:
            raise ValueError(
                f"DemoNet can't serialize {type(obj).__name__!r}: {obj!r}"
            ) from ex

    def to_graph(self):
        "Create a pygraphviz Graph of the network."
        if pgv is None:
            raise RuntimeError("ERROR: pygraphviz is not installed.")

        graph = pgv.AGraph(
            **_PyGraphStyle.graph,  # pyright: ignore[reportGeneralTypeIssues]
        )

        for item in self.items:
            match item:
                case Switch():
                    graph.add_node(item.name, **_PyGraphStyle.switch)
                case Host():
                    sublabels = [item.name, item.assigned_ipv4, item.assigned_ipv6]
                    host_label = "\n".join(x for x in sublabels if x)
                    graph.add_node(
                        item.name,
                        label=host_label,
                        **_PyGraphStyle.host,
                    )
                    if item.switch:
                        graph.add_edge(
                            item.name,
                            item.switch,
                            headlabel=f"{item.assigned_switch_port}",
                            **_PyGraphStyle.link,
                        )
                case Bridge():
                    sublabels = [item.name, item.ipv4]
                    bridge_label = "\n".join(x for x in sublabels if x)
                    graph.add_node(
                        item.name,
                        label=bridge_label,
                        **_PyGraphStyle.bridge,
                    )
                case Link():
                    labels = {}
                    if item.assigned_end_port:
                        labels["headlabel"] = str(item.assigned_end_port)
                    if item.assigned_start_port:
                        labels["taillabel"] = str(item.assigned_start_port)
                    style = _PyGraphStyle.link.copy()
                    if item.style:
                        style.update(style=item.style)
                    graph.add_edge(
                        item.start,
                        item.end,
                        **labels,  # pyright: ignore[reportUnknownArgumentType]
                        **style,
                    )
                case _:
                    pass

        return graph


PID_MATCH = re.compile(r"<\w+ (\w+):.* pid=(\d+)>", re.MULTILINE)


class _AContextHelper:
    "Helper class for implementing an async context manager class."

    __context: Any = None

    async def __aenter__(self):
        assert self.__context is None
        context = contextlib.asynccontextmanager(self._async_context_)()
        result = await context.__aenter__()
        self.__context = context
        return result

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        context = self.__context
        self.__context = None
        return await context.__aexit__(exc_type, exc_value, exc_tb)

    async def _async_context_(self):
        yield self  # subclass must override


class DemoNet(_AContextHelper):
    """Demo network that controls Mininet running in a container.

    ```
        config = [
            Image("docker.io/opennetworking/p4mn"),
            Switch("s1"),
            Host("h1", "s1"),
            Host("h2", "s1"),
        ]

        async with DemoNet(config) as net:
            await net.pingall()
    ```
    """

    config: Config
    _pids: dict[str, int]
    _config_file: Path
    _prompt: Prompt | None = None

    def __init__(
        self,
        config: Config | Sequence[Directive],
    ):
        if isinstance(config, Config):
            self.config = config
        else:
            self.config = Config(config)
        self._pids = {}
        self._config_file = _LOCAL_TEMP_DIR / "demonet_config.json"
        self._config_file.write_text(self.config.to_json())

    async def _async_context_(self):
        assert self._prompt is None
        cmd = await self._mininet_command()

        # FIXME: Remove Runner wrapper on next line.
        async with Runner(cmd.stdout(sh.CAPTURE)) as run:
            self._prompt = Prompt(run, "mininet> ", normalize_newlines=True)
            await self._read_welcome()
            await self._read_pids()
            yield self

            await self._read_exit()
            self._prompt = None

    async def _read_welcome(self):
        "Collect welcome message from Mininet."
        assert self._prompt is not None
        welcome = await self._prompt.receive()
        if welcome.startswith("Error:"):
            raise RuntimeError(welcome)
        print(welcome)

    async def _read_pids(self):
        "Retrieve the PID's so we can do our own `mnexec`."
        dump = await self.send("dump")
        for mo in PID_MATCH.finditer(dump):
            name, pid = mo.groups()
            self._pids[name] = int(pid)
        print(self._pids)

    async def _read_exit(self):
        "Exit and collect exit message from Mininet."
        assert self._prompt is not None
        print(await self._prompt.send("exit"))

    async def run_interactively(self):
        cmd = await self._mininet_command()
        await cmd.stdin(sh.INHERIT).stdout(sh.INHERIT).stderr(sh.INHERIT)

    async def send(self, cmdline: str, *, expect: str = "") -> str:
        assert self._prompt is not None
        result = await self._prompt.send(cmdline)
        print(result)
        if expect:
            assert expect in result
        return result

    async def _mininet_command(self):
        """Return a command to run Mininet.

        If Mininet is installed locally, we return a command to run the local
        version. Otherwise, we set up a Docker image to run Mininet in a
        container.
        """
        if sh.find_command("mn"):
            return mininet_start(DEMONET_CONFIG=str(self._config_file))

        image = self.config.image()
        switch_count = self.config.switch_count()
        container = f"mininet-{int(time.time()):x}"

        await podman_check()
        await podman_create(container, image.name, switch_count)
        await podman_copy(_LOCAL_TOPO_PY, container, _IMAGE_TOPO_PY)
        await podman_copy(self._config_file, container, _IMAGE_CONFIG)

        return podman_start(container, DEMONET_CONFIG=str(_IMAGE_CONFIG))


_podman = Path("podman")

_LOCAL_TEMP_DIR = Path("/tmp")
_LOCAL_TOPO_PY = Path(__file__).parent / "demonet_topo.py"
_LOCAL_P4SWITCH_PY = Path(__file__).parent.parent.parent / "ci/demonet/p4switch.py"

assert _LOCAL_TOPO_PY.exists()
assert _LOCAL_P4SWITCH_PY.exists()

PUBLISH_BASE = 50000

_IMAGE_TOPO_PY = Path("/tmp/demonet_topo.py")
_IMAGE_CONFIG = Path("/tmp/demonet_config.json")


async def podman_check():
    "Check the versions of podman/docker installed."
    global _podman

    cmd = sh.find_command("podman") or sh.find_command("docker")
    if cmd is None:
        raise RuntimeError("Cannot find podman or docker!")

    _podman = cmd

    # Do a quick check that podman/docker is available.
    if not await sh.result(_podman, "ps"):
        raise RuntimeError(f"There is a problem using docker/podman: {cmd}")


def extra_mininet_args(*, debug: bool, topo_py: Path):
    return (
        "--custom",
        topo_py,
        "--topo",
        "demonet",
        ("-v", "debug") if debug else (),
    )


def mininet_start(**env: str):
    debug = bool(os.environ.get("DEMONET_DEBUG"))

    return (
        sh(
            "mn",
            "--custom",
            _LOCAL_P4SWITCH_PY,
            "--switch",
            "bmv2",
            "--controller",
            "none",
            extra_mininet_args(debug=debug, topo_py=_LOCAL_TOPO_PY),
        )
        .set(pty=True)
        .env(**env)
    )


def podman_create(
    container: str,
    image_slug: str,
    switch_count: int,
) -> Command[str]:
    assert switch_count > 0

    if switch_count == 1:
        publish = f"{PUBLISH_BASE + 1}"
    else:
        publish = f"{PUBLISH_BASE + 1}-{PUBLISH_BASE+switch_count}"

    debug = bool(os.environ.get("DEMONET_DEBUG"))

    return sh(
        _podman,
        "create",
        "--privileged",
        "--rm",
        "-it",
        "--name",
        container,
        "--publish",
        f"{publish}:{publish}",
        image_slug,
        extra_mininet_args(debug=debug, topo_py=_IMAGE_TOPO_PY),
    )


def podman_copy(src_path: Path, container: str, dest_path: Path) -> Command[str]:
    return sh(_podman, "cp", src_path, f"{container}:{dest_path}")


def podman_start(container: str, **env: str) -> Command[str]:
    return sh(_podman, "start", "-ai", container).set(pty=True).env(**env)


def run(config: Sequence[Directive]) -> None:
    "Create demo network and run it interactively."

    async def _main():
        net = DemoNet(config)
        await net.run_interactively()

    asyncio.run(_main())


class _ConfigPortDB:
    "Helper class to help track the next available switch port number."

    _next_port: dict[str, int]

    def __init__(self):
        self._next_port = {}

    def add_switch(self, name: str) -> None:
        if name in self._next_port:
            raise ValueError(f"duplicate switch named {name!r}")
        self._next_port[name] = 1

    def next_port(self, name: str) -> int:
        result = self._next_port[name]
        self._next_port[name] = result + 1
        return result

    def __contains__(self, name: str) -> bool:
        return name in self._next_port


def _parse_args():
    "Create argument parser and parse arguments."
    parser = argparse.ArgumentParser("demonet")
    parser.add_argument("--draw", help="Draw network map into file.")
    return parser.parse_args()


def main(config: Sequence[Directive]) -> None:
    "Main entry point for demonet."
    args = _parse_args()
    if args.draw:
        Config(config).draw(args.draw)
    else:
        run(config)


def _get_local_ipv4_address():
    "Retrieve the local (route-able) IPv4 address."
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(0)
        sock.connect(("10.254.254.254", 1))
        result = sock.getsockname()[0]
    finally:
        sock.close()
    return result


_LOCAL_IP = _get_local_ipv4_address()


class _PyGraphStyle:
    "Style defaults for different graphviz elements."

    graph = dict(
        bgcolor="lightblue",
        margin="0",
        pad="0.25",
    )

    switch = dict(
        shape="box",
        fillcolor="green:white",
        style="filled",
        gradientangle=90,
        width="0.1",
        height="0.1",
        margin="0.08,0.02",
    )

    host = dict(
        shape="box",
        width="0.01",
        height="0.01",
        margin="0.04,0.02",
        fillcolor="yellow:white",
        style="filled",
        gradientangle=90,
        fontsize="10",
    )

    bridge = dict(
        shape="box",
        width="0.01",
        height="0.01",
        margin="0.04,0.02",
        fillcolor="white",
        style="filled",
        fontsize="10",
    )

    link = dict(
        penwidth="2.0",
        fontcolor="darkgreen",
        fontsize="10",
    )
