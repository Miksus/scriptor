
.. meta::
   :description: Red Box is an advanced email reading for Python.
   :keywords: CLI, Python, subprocess, command-line, program

.. raw:: html
   :file: header.html

- `Documentation <https://scriptor.readthedocs.io/>`_
- `Source code (Github) <https://github.com/Miksus/scriptor>`_
- `Releases (PyPI) <https://pypi.org/project/scriptor/>`_


Why Scriptor?
-------------

Scriptor is a high-level abstraction for ``subprocess`` and ``async.subprocess``.
Scriptor makes it easy to execute command-line programs from Python.

Features:

- Run programs sync or async using the same syntax
- High-level program abstraction
- Easy program parametrization

A simple example:

.. code-block:: python

    >>> from scriptor import Program
    >>> python = Program('python3')

    >>> # Run a program (and wait for finish)
    >>> python('myscript.py')

You can also conveniently parametrize programs:

.. code-block:: python

    >>> # Run: python3 myscript.py --report_date 2022-01-01
    >>> python('myscript.py', report_date="2022-01-01")

You can create convenient interfaces to other programs
with Scriptor. See: 

- :ref:`Git interface <cookbook-git>`

Interested?
-----------

Install the package:

.. code-block:: console

    pip install scriptor


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index
   cookbook/index
   versions


Indices and tables
==================

* :ref:`genindex`
