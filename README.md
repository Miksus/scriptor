
# WIP: Scriptor
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

## More Examples

There is also a query language for arbitrary search queries:

```python
>>> from scriptor import Program
>>> python = Program("python")

>>> # Call the program (and wait for finish)
>>> python("myscript.py")
```

Same with async:

```python
>>> from scriptor import Program
>>> python = Program("python")

>>> # Call the program (and wait for finish)
>>> await python.call_async("myscript.py")
```

---

See more from the documentation.

If the library helped you, consider buying a coffee for the maintainer ☕.

## Author

* **Mikael Koli** - [Miksus](https://github.com/Miksus) - koli.mikael@gmail.com

