import asyncio
from textwrap import dedent
import sys
from time import time, sleep
import platform

import pytest

from scriptor.runner import run_process_sync, run_process_iter, run_process_async

IS_WINDOWS = platform.system() == "Windows"

def test_run_sync():
    code = dedent("""
        print('Hello')
        print('world')
        """)
    output = run_process_sync([sys.executable, "-c", code])
    if IS_WINDOWS:
        assert output == b"Hello\r\nworld\r\n"
    else:
        assert output == b"Hello\nworld\n"

def test_run_iter(tmpdir):
    code = dedent("""
        print('Hello')
        print('world')
        """)
    lines = []
    for line in run_process_iter([sys.executable, "-c", code]):
        lines.append(line)
    if IS_WINDOWS:
        assert lines == [b"Hello\r\n", b"world\r\n"]
    else:
        assert lines == [b"Hello\n", b"world\n"]

@pytest.mark.asyncio
async def test_run_async(tmpdir):
    code = dedent("""
        print('Hello')
        print('world')
        """)
    output = await run_process_async([sys.executable, "-c", code])
    if IS_WINDOWS:
        assert output == b"Hello\r\nworld\r\n"
    else:
        assert output == b"Hello\nworld\n"

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

def test_run_iter_running(tmpdir):
    # Check the program is still running when
    # iter returns rows
    file = tmpdir.join("myfile.py")
    file.write(dedent("""
        from time import sleep
        from time import time
        print(time())
        sleep(0.2)
        print(time())
        sleep(0.2)
        print(time())
        """))

    obs_count = 0
    last_check = time()
    for obs in run_process_iter([sys.executable, file]):
        print("Observation:", obs)
        obs = float(obs.decode("UTF-8"))
        assert obs > last_check
        last_check = time()
        obs_count += 1
    assert obs_count == 3