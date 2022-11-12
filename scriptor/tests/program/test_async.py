import asyncio
import io
import json
import sys
import platform
from textwrap import dedent
import time

import pytest
from scriptor.process import ProcessError
from scriptor.program import Program



@pytest.mark.asyncio
async def test_run(tmpdir):
    # Test run actually does not wait till the end
    # of the process to return the execution

    # We check that we can run a function in between the
    # process execution

    async def do_other():
        await asyncio.sleep(0.1)
        return time.time()

    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import time
        print(time.time())
        time.sleep(0.5)
        print(time.time())
        """
    ))

    python = Program(sys.executable)

    task_run = asyncio.create_task(python.run_async(py_file))
    task_check = asyncio.create_task(do_other())

    output = await task_run
    time_check = await task_check

    output = output.split("\n")
    time_start, time_finish = float(output[0]), float(output[1])

    assert time_start < time_check 
    assert time_check < time_finish