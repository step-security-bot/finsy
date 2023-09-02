import asyncio
from pathlib import Path

import pytest

TLSDEMO_DIR = Path(__file__).parent.parent / "tls_demo"

DEMONET = TLSDEMO_DIR / "net/run.py"


@pytest.mark.xfail(reason="requires updated image")
async def test_demo1(demonet, python):
    "Test the tls_demo/demo1 example program."
    async with python(TLSDEMO_DIR / "demo1.py") as demo1:
        await asyncio.sleep(0.25)
        await demonet.send("pingall", expect="(2/2 received)")
        demo1.cancel()
