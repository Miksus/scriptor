import io
import json
import sys
import platform
from textwrap import dedent

import pytest
from scriptor.process import ProcessError
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
    if sync:
        output = python("-V")
    else:
        output = await python.call_async("-V")
    assert output == f"Python {version}"

@param_async
async def test_success(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        ...
        """
    ))

    python = Program(sys.executable)
    if sync:
        output = python(py_file)
    else:
        output = await python.call_async(py_file)
    assert output is None

@param_async
@pytest.mark.parametrize("how", ['default', 'string', 'type'])
async def test_success_output(tmpdir, how, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print("Hello")
        print("world")
        """
    ))

    if how == 'argument':
        python = Program(sys.executable, output_type=str)
    else:
        python = Program(sys.executable)

    output = python(py_file) if sync else await python.call_async(py_file)
    assert output == "Hello\nworld"

@param_async
@pytest.mark.parametrize("how", ['string', 'type'])
async def test_success_output_bytes(tmpdir, how, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print("Hello")
        print("world")
        """
    ))

    output_type = 'bytes' if how == "string" else bytes
    python = Program(sys.executable, output_type=output_type)
    output = python(py_file) if sync else await python.call_async(py_file)
    if IS_WINDOWS:
        assert output == b"Hello\r\nworld\r\n"
    else:
        assert output == b"Hello\nworld\n"

@param_async
async def test_error(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print("Hello")
        print("world")
        raise RuntimeError("Oops")
        """
    ))

    python = Program(sys.executable)
    with pytest.raises(ProcessError) as exc_info:
        python(py_file) if sync else await python.call_async(py_file)
    exc = exc_info.value
    tb = exc_info.tb
    assert str(exc).endswith('raise RuntimeError("Oops")\nRuntimeError: Oops')

    assert exc.stdout == "Hello\nworld"
    assert exc.returncode == 1

@param_async
async def test_kwargs_long(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import sys
        assert sys.argv[1:] == ["--report_date", "2022-01-01"]
        print("Success")
        """
    ))
    python = Program(sys.executable)
    if sync:
        output = python(py_file, report_date="2022-01-01")
    else:
        output = await python.call_async(py_file, report_date="2022-01-01")
    assert output == "Success"

@param_async
async def test_kwargs_short(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import sys
        assert sys.argv[1:] == ["-rd", "2022-01-01"]
        print("Success")
        """
    ))

    python = Program(sys.executable)
    if sync:
        output = python(py_file, rd="2022-01-01")
    else:
        output = await python.call_async(py_file, rd="2022-01-01")
    assert output == "Success"

@param_async
async def test_custom_output(tmpdir, sync):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print('{"name":"John", "age":30, "car":null}')
        """
    ))

    python = Program(sys.executable, output_parser=lambda x: json.loads(x))

    output = python(py_file) if sync else await python.call_async(py_file)
    assert output == {"name": "John", "age": 30, "car": None}

@param_async
async def test_custom_output_bytes(tmpdir, sync):
    def parse_bytes(x):
        assert isinstance(x, bytes)
        return x
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        print("Hello world")
        """
    ))
    python = Program(sys.executable, output_parser=parse_bytes, output_type=bytes)
    output = python(py_file) if sync else await python.call_async(py_file)
    if IS_WINDOWS:
        assert output == b"Hello world\r\n"
    else:
        assert output == b"Hello world\n"

@param_async
@pytest.mark.parametrize("buffer", ["bytes", "string"])
async def test_input(tmpdir, sync, buffer):
    def parse_bytes(x):
        assert isinstance(x, bytes)
        return x
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        i = input()
        assert i == "Hello"
        print("Hello world")
        """
    ))
    python = Program(sys.executable, output_parser=parse_bytes, output_type=bytes)

    buff = Input(b'Hello') if buffer == "bytes" else Input('Hello')
    output = python(py_file, buff) if sync else await python.call_async(py_file, buff)

    if IS_WINDOWS:
        assert output == b"Hello world\r\n"
    else:
        assert output == b"Hello world\n"

@param_async
@pytest.mark.parametrize("buffer", ["bytes", "string"])
@pytest.mark.parametrize("cli_args", ["before", "after"])
async def test_input_with_arg(tmpdir, sync, buffer, cli_args):
    def parse_bytes(x):
        assert isinstance(x, bytes)
        return x
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import sys
        args = sys.argv[1:]
        i = input()
        assert i == "Hello"
        print(*args)
        """
    ))
    python = Program(sys.executable, output_parser=parse_bytes, output_type=bytes)

    buff = Input(b'Hello') if buffer == "bytes" else Input('Hello')
    if cli_args == "before":
        args = (py_file, 'Hello', 'world', buff)
    else:
        args = (py_file, buff, 'Hello', 'world')
    output = python(*args) if sync else await python.call_async(*args)

    if IS_WINDOWS:
        assert output == b"Hello world\r\n"
    else:
        assert output == b"Hello world\n"