.. _cookbook-python:

Python
======

There is a built-in Python program class for 
convenience:

.. code-block:: python

    >>> from scriptor.builtin import Python
    >>> python = Python('.../env/bin/python')

You can also use your current interpreter or 
the base interpreter:

.. code-block:: python

    >>> from scriptor.builtin import current_python, base_python

In addition to other methods ``Program`` has, Python
instances also have some additional features: 

.. code-block:: python

    >>> # Inspect the interpreter
    >>> python.version
    "Python 3.8.10"
    >>> python.full_version
    "Python 3.8.10 ..."

    >>> # Run code
    >>> python.run_script("path/to/myscript.py")
    >>> python.run_module("path.to.myscript")
    >>> python.run_code("print('Hello world')")
    "Hello world"