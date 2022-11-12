import sys
from textwrap import dedent
from scriptor.builtin import current, python

def test_current():
    assert current.program == (sys.executable,)

def test_python(tmpdir):
    tmpdir.mkdir("files")
    py_file = tmpdir.join("files/myscript.py")
    py_file.write(dedent("""
        print("Hello world")
        """))

    assert current.run_code("print('Hello world')") == 'Hello world'

    assert current.version.startswith("Python 3.")
    assert current.full_version.startswith("Python 3.")

    assert current.run_script(py_file) == "Hello world"


    assert current.use(cwd=tmpdir).run_module("files.myscript") == "Hello world"