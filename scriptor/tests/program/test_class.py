import io
import json
import sys
import platform
from textwrap import dedent

import pytest
from scriptor.process import ProcessError
from scriptor import Program, BaseProgram

def param_async(func):
    mark_async = pytest.mark.asyncio
    mark_params = pytest.mark.parametrize('sync', [pytest.param(True, id="sync"), pytest.param(False, id="async")])

    return mark_async(mark_params(func))


def test_args_with_init(tmpdir):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import sys
        assert sys.argv[1:] == ["Hello", "world", "arg"]
        """
    ))

    python = Program(sys.executable, py_file, "Hello", "world")
    output = python("arg")
    assert output is None

def test_kwargs_with_init(tmpdir):
    py_file = tmpdir.join("myfile.py")
    py_file.write(dedent("""
        import sys
        assert sys.argv[1:] == ["--default", "val1", "--override", "val3"]
        """
    ))

    python = Program(sys.executable, default_kwargs={"default": "val1", "override": "val2"})
    output = python(py_file, override="val3")
    assert output is None

def test_subclass():

    # Test subclass
    class MyProgram(BaseProgram):
        program = "python"

    program = MyProgram()
    assert program(c="print('Hello')") == 'Hello'
    
    # Test the program accepts a list
    class MyProgram(BaseProgram):
        program = ["python", "-c", "print('Hello')"]

    program = MyProgram()
    assert program() == 'Hello'

def test_subclass_default_kwargs():

    class MyProgram(BaseProgram):
        program = "python"
        default_kwargs = {'c': "print('Hello')"}

    program = MyProgram()
    assert program() == 'Hello'
    assert program(c="print('world')") == 'world'
    