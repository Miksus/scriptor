import asyncio
from textwrap import dedent
import sys
from time import time

import pytest

from scriptor.runner import run_process_sync, run_process_iter, run_process_async

def test_run_sync():
    output = run_process_sync([sys.executable, "-V"])
    assert output.startswith("Python 3")

def test_run_iter(tmpdir):
    code = dedent("""
        print('Hello')
        print('world')
        """)
    lines = []
    for line in run_process_iter([sys.executable, "-c", code]):
        lines.append(line)
    assert lines == ["Hello\n", "world\n"]

@pytest.mark.asyncio
async def test_run_async(tmpdir):
    code = dedent("""
        print('Hello')
        print('world')
        """)
    output = await run_process_async([sys.executable, "-c", code])
    assert output == "Hello\r\nworld\r\n"

@pytest.mark.asyncio
async def test_run_async_timeout(tmpdir):
    code = dedent("""
        from time import sleep
        print('Hello')
        sleep(5)
        print('world')
        """)
    with pytest.raises(asyncio.exceptions.TimeoutError):
        output = await run_process_async([sys.executable, "-c", code], timeout=0.1)
