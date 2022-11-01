"""
Finsy demo program for a simple P4Runtime controller that floods every packet.
Incoming packets are copied and delivered to all other ports using a 
P4MulticastGroupEntry. In addition, copies of all packets are sent to the
controller as P4PacketIn messages.
"""

import asyncio
import logging
import signal
from pathlib import Path

import finsy as fy

# P4SRC is the path to the "p4src" directory in the same directory as demo1.py.
P4SRC = Path(__file__).parent / "p4src"

# LOG is a logger that will include the current asyncio task name. The task
# name includes the name of the switch, so you don't have to include that
# information when you log a message.
LOG = fy.LoggerAdapter(logging.getLogger("demo1"))


async def ready_handler(sw: fy.Switch):
    """The `ready_handler` function is the main entry point for each switch.

    Finsy calls this automatically after it has connected to the switch and
    loaded the forwarding pipeline program.
    """
    await sw.delete_all()
    await sw.write(
        [
            # Insert multicast group with ports 1, 2, 3 and CONTROLLER.
            +fy.P4MulticastGroupEntry(1, replicas=[1, 2, 3, 255]),
            # Modify default table entry to flood all unmatched packets.
            ~fy.P4TableEntry(
                "ipv4",
                action=fy.P4TableAction("flood"),
                is_default_action=True,
            ),
        ]
    )

    async for packet in sw.read_packets():
        LOG.info("%r", packet)


async def main():
    "Main program."

    # Boilerplate to shutdown cleanly upon SIGTERM signal.
    asyncio.get_running_loop().add_signal_handler(
        signal.SIGTERM,
        lambda task: task.cancel(),
        asyncio.current_task(),
    )

    # Shared settings for all P4Runtime switches.
    options = fy.SwitchOptions(
        p4info=P4SRC / "hello.p4info.txt",
        p4blob=P4SRC / "hello.json",
        ready_handler=ready_handler,
    )

    switches = [
        fy.Switch("sw1", "127.0.0.1:50001", options),
        fy.Switch("sw2", "127.0.0.1:50002", options),
        fy.Switch("sw3", "127.0.0.1:50003", options),
    ]

    controller = fy.Controller(switches)
    await controller.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
