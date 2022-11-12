import asyncio
import io
import signal
import time
import sys
import platform
from textwrap import dedent

import pytest
from scriptor.process import Process, AsyncProcess, ProcessError
from scriptor.program import Program, Input

IS_WINDOWS = platform.system() == "Windows"

def param_async(func):
    mark_async = pytest.mark.asyncio
    mark_params = pytest.mark.parametrize('sync', [pytest.param(True, id="sync"), pytest.param(False, id="async")])

    return mark_async(mark_params(func))

@param_async
async def test_arg(sync):
    python = Program(sys.executable)
    version = platform.python_version()
    process = python.start("-V") if sync else await python.start_async("-V")
    if sync:
        process.wait()
    else:
        await process.wait()
    output = process.read() if sync else await process.read()
    assert output == f"Python {version}"

    # Test repeated read
    output = process.read() if sync else await process.read()
    assert output == f"Python {version}"

@param_async
async def test_error(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        raise RuntimeError("Oops")
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    assert isinstance(process, Process) if sync else isinstance(process, AsyncProcess)

    process.wait() if sync else await process.wait()
    assert process.returncode == 1

    # Test stdout and stderr
    stdout = process.get_stdout() if sync else await process.get_stdout()
    assert stdout == b""

    stderr = process.get_stderr() if sync else await process.get_stderr()
    stderr_str = stderr.decode("UTF-8")
    if IS_WINDOWS:
        assert stderr_str.endswith("RuntimeError: Oops\r\n")
    else:
        assert stderr_str.endswith("RuntimeError: Oops\n")

@param_async
async def test_error_raise(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        raise RuntimeError("Oops")
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    assert isinstance(process, Process) if sync else isinstance(process, AsyncProcess)

    process.wait() if sync else await process.wait()
    with pytest.raises(ProcessError) as exc_info:
        if sync:
            process.raise_for_return()
        else:
            await process.raise_for_return()
    assert process.returncode == 1

    error_message = str(exc_info.value)
    assert error_message.endswith("RuntimeError: Oops")

    # Test stdout and stderr are still there
    stdout = process.get_stdout() if sync else await process.get_stdout()
    assert stdout == b""

    stderr = process.get_stderr() if sync else await process.get_stderr()
    stderr_str = stderr.decode("UTF-8")
    if IS_WINDOWS:
        assert stderr_str.endswith("RuntimeError: Oops\r\n")
    else:
        assert stderr_str.endswith("RuntimeError: Oops\n")

@param_async
async def test_success(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        ...
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    assert isinstance(process, Process) if sync else isinstance(process, AsyncProcess)

    process.wait() if sync else await process.wait()
    assert process.returncode == 0

    output = process.read() if sync else await process.read()
    assert output is None

    # Test repeated read
    output = process.read() if sync else await process.read()
    assert output is None

@param_async
async def test_success_output(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print("Hello")
        print("world")
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)

    process.wait() if sync else await process.wait()
    output = process.read() if sync else await process.read()
    assert process.returncode == 0
    assert output == "Hello\nworld"

    # Test repeated read
    output = process.read() if sync else await process.read()
    assert process.returncode == 0
    assert output == "Hello\nworld"

    # Test stdout and stderr
    stdout = process.get_stdout() if sync else await process.get_stdout()
    if IS_WINDOWS:
        assert stdout == b"Hello\r\nworld\r\n"
    else:
        assert stdout == b"Hello\nworld\n"

    stderr = process.get_stderr() if sync else await process.get_stderr()
    assert stderr == b""

@param_async
async def test_success_finish(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        ...
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    while process.running:
        assert process.returncode is None
        if sync:
            time.sleep(0.01)
        else:
            await asyncio.sleep(0.01)
    assert process.returncode == 0

@param_async
@pytest.mark.parametrize("how", ['kill', 'terminate', 'signal'])
async def test_interupt(tmpdir, sync, how):

    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import time
        time.sleep(5)
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    
    if how == "kill":
        process.kill()
        process.wait() if sync else await process.wait()
        assert process.returncode != 0
    elif how == "terminate":
        process.terminate()
        process.wait() if sync else await process.wait()
        assert process.returncode != 0
    elif how == "signal":
        process.send_signal(signal.SIGTERM)
        process.wait() if sync else await process.wait()
        assert process.returncode != 0

    # Check the process is not running either
    assert process.returncode is not None

@param_async
async def test_input(tmpdir, sync):

    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        i = input()
        assert i == "Hello"
        print("Hello world")
        """
    ))
    python = Program(sys.executable)
    process = python.start(py_file, Input('Hello')) if sync else await python.start_async(py_file, Input('Hello'))

    process.wait() if sync else await process.wait()
    output = process.read() if sync else await process.read()

    assert process.finished
    assert output == "Hello world"

@param_async
async def test_input_write(tmpdir, sync):

    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        i = input()
        assert i == "Hello"
        print("Hello world")
        """
    ))
    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)
    process.write(b'Hello')

    process.wait() if sync else await process.wait()
    output = process.read() if sync else await process.read()

    assert process.finished
    assert output == "Hello world"

@param_async
@pytest.mark.parametrize("how", ['kill', 'terminate', 'signal'])
async def test_process_attrs(tmpdir, sync, how):

    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import time
        time.sleep(5)
        """
    ))

    python = Program(sys.executable)
    process = python.start(py_file) if sync else await python.start_async(py_file)

    assert repr(process)
    assert process.stdin
    assert process.stdout
    assert process.stderr