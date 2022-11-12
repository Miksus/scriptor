import sys
from textwrap import dedent
from scriptor.builtin import current_python, base_python, Python

def test_current():
    assert current_python.program == (sys.executable,)

def test_python_run(tmpdir):
    tmpdir.mkdir("files")
    py_file = tmpdir.join("files/myscript.py")
    py_file.write(dedent("""
        print("Hello world")
        """))

    assert current_python.run_code("print('Hello world')") == 'Hello world'
    assert current_python.run_script(py_file) == "Hello world"
    assert current_python.use(cwd=tmpdir).run_module("files.myscript") == "Hello world"

def test_python_attrs():
    assert current_python.version.startswith("Python 3.")
    assert current_python.full_version.startswith("Python 3.")
    assert current_python.help.startswith("usage: ")