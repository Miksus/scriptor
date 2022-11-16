import sys
from textwrap import dedent

import pytest
from scriptor.process import ProcessError
from scriptor import Program, BaseProgram

def test_use_cwd(tmpdir):
    tmpdir.mkdir("mydir")
    py_file = tmpdir.join("mydir/myfile.py")
    py_file.write(dedent("""
        import os
        from pathlib import Path
        assert Path(os.getcwd()).name == "mydir"
        print("Hello")
        """
    ))

    python = Program(sys.executable)
    python_in_dir = python.use(cwd=tmpdir / "mydir")
    with pytest.raises(ProcessError):
        python(py_file)

    output = python_in_dir(py_file)
    assert output == "Hello"

    assert python.cwd is None
    assert python_in_dir.cwd == tmpdir / "mydir"

def test_use_not_found():
    python = Program(sys.executable)
    with pytest.raises(AttributeError):
        python.use(non_existent="value")

def test_init():
    python = Program(sys.executable, timeout=20, cwd="path/to/script", env={"MY_VAR": "a value"})
    assert python.timeout == 20
    assert python.cwd == "path/to/script"
    assert python.env == {"MY_VAR": "a value"}

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
    