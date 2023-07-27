import importlib.util
import json

import pytest

import finsy.test.demonet as dn


def _has_pygraphviz():
    "Return True if the `pygraphviz` module is available."
    return importlib.util.find_spec("pygraphviz") is not None


def test_config():
    "Test the DemoNet Config object."
    config = dn.Config(
        [
            dn.Switch("s1"),
            dn.Host("h1", "s1"),
            dn.Host("h2", ipv6="auto"),
            dn.Link("s1", "h2"),
        ]
    )

    assert len(config.items) == 4
    assert config.image() == dn.Image("docker.io/opennetworking/p4mn")
    assert config.switch_count() == 1

    assert json.loads(config.to_json(indent=2)) == [
        {"name": "s1", "kind": "switch", "params": {}, "commands": []},
        {
            "name": "h1",
            "switch": "s1",
            "kind": "host",
            "ifname": "eth0",
            "mac": "auto",
            "ipv4": "auto",
            "ipv4_gw": "",
            "ipv6": "",
            "ipv6_gw": "",
            "ipv6_linklocal": False,
            "static_arp": {},
            "disable_offload": ["tx", "rx", "sg"],
            "commands": [],
            "assigned_switch_port": 1,
            "assigned_mac": "00:00:00:00:00:01",
            "assigned_ipv4": "10.0.0.1/8",
            "assigned_ipv6": "",
        },
        {
            "name": "h2",
            "switch": "",
            "kind": "host",
            "ifname": "eth0",
            "mac": "auto",
            "ipv4": "auto",
            "ipv4_gw": "",
            "ipv6": "auto",
            "ipv6_gw": "",
            "ipv6_linklocal": False,
            "static_arp": {},
            "disable_offload": ["tx", "rx", "sg"],
            "commands": [],
            "assigned_switch_port": 0,
            "assigned_mac": "00:00:00:00:00:02",
            "assigned_ipv4": "10.0.0.2/8",
            "assigned_ipv6": "fc00::2/64",
        },
        {
            "start": "s1",
            "end": "h2",
            "kind": "link",
            "style": "",
            "commands": [],
            "assigned_start_port": 2,
            "assigned_end_port": 0,
        },
    ]


@pytest.mark.skipif(not _has_pygraphviz(), reason="requires pygraphviz")
def test_config_render_dot():
    "Test rendering the configuration as a dot file."
    config = dn.Config(
        [
            dn.Switch("s1"),
            dn.Host("h1", "s1"),
            dn.Host("h2", ipv6="auto"),
            dn.Link("s1", "h2"),
        ]
    )

    result = config.to_graph().to_string()
    assert (
        result.strip().expandtabs(2)
        == r"""
strict graph "" {
  graph [bgcolor=lightblue,
    margin=0,
    pad=0.25
  ];
  node [label="\N"];
  s1  [fillcolor="green:white",
    gradientangle=90,
    height=0.1,
    margin="0.08,0.02",
    shape=box,
    style=filled,
    width=0.1];
  h2  [fillcolor="yellow:white",
    fontsize=10,
    gradientangle=90,
    height=0.01,
    label="h2
10.0.0.2/8
fc00::2/64",
    margin="0.04,0.02",
    shape=box,
    style=filled,
    width=0.01];
  s1 -- h2  [fontcolor=darkgreen,
    fontsize=10,
    penwidth=2.0,
    taillabel=2];
  h1  [fillcolor="yellow:white",
    fontsize=10,
    gradientangle=90,
    height=0.01,
    label="h1
10.0.0.1/8",
    margin="0.04,0.02",
    shape=box,
    style=filled,
    width=0.01];
  h1 -- s1  [fontcolor=darkgreen,
    fontsize=10,
    headlabel=1,
    penwidth=2.0];
}""".strip()
    )
