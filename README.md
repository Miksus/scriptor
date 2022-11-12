
# Scriptor
> Run programs with command-line interface with Python

---

[![Pypi version](https://badgen.net/pypi/v/scriptor)](https://pypi.org/project/scriptor/)
[![build](https://github.com/Miksus/scriptor/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Miksus/scriptor/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Miksus/scriptor/branch/master/graph/badge.svg?token=IMR1CQT9PY)](https://codecov.io/gh/Miksus/scriptor)
[![Documentation Status](https://readthedocs.org/projects/scriptor/badge/?version=latest)](https://scriptor.readthedocs.io)
[![PyPI pyversions](https://badgen.net/pypi/python/scriptor)](https://pypi.org/project/scriptor/)

- [Documentation](https://scriptor.readthedocs.io)
- [Source code](https://github.com/Miksus/scriptor)
- [Releases](https://pypi.org/project/scriptor/)

## What is it?
Scriptor is a high-level library for command-line.
Scriptor makes it easy to integrate other CLI programs to your Python application.

Core features:

- Run programs sync or async using same syntax
- High-level program abstraction
- Easy program parametrization

Install it from PyPI:

```shell
pip install scriptor
```

## Why Scriptor?

Scriptor abstracts ``subprocess`` and ``asyncio.subprocess``
to the same syntax making it easy to use both of them and 
switch between.  

```python
>>> from scriptor import Program
>>> python = Program("python3")

>>> # Call the program (and wait for finish)
>>> python("myscript.py")
```

## More Examples

Here are some examples:

```python
>>> # Parametrize a script
>>> python("myscript.py", report_date="2022-11-11")

>>> # Use different current working directory
>>> python.use(cwd="path/to/dir")("myscript.py")

>>> # Run script with output (in stdout)
>>> python("print_hello.py")
'Hello world'

>>> # Run failing script
>>> python("failing.py")
Traceback (most recent call last):
...
scriptor.process.ProcessError: Traceback (most recent call last):
  File "failing.py", line 1, in <module>
    raise RuntimeError("Oops!")
RuntimeError: Oops!
```

Examples to start a process:

```python
>>> process = python.start("print_hello.py")
>>> process.finished
False

>>> # Wait for the process to finish
>>> process.wait()

>>> # Raise error if process failed
>>> process.raise_for_return()

>>> # Read the results
>>> process.read()
'Hello world'
```

and some more with async:

```python
>>> # Parametrize a script
>>> await python.call_async("myscript.py", report_date="2022-11-11")

>>> # Run script with output (in stdout)
>>> await python.call_async("print_hello.py")
'Hello world'

```

and example to start async:

```python
>>> process = await python.start_async("print_hello.py")
>>> process.finished
False

>>> # Wait for the process to finish
>>> process.wait()

>>> # Raise error if process failed
>>> process.raise_for_return()

>>> # Read the results
>>> process.read()
'Hello world'
```

---

See more from the documentation.

If the library helped you, consider buying a coffee for the maintainer ☕.

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

