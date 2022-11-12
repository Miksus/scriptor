
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
Scriptor makes it easy to run and communicate with external programs. 

Features:

- High-level abstraction to run programs
- Convenient program parametrization and output parsing
- Full async support

A simple example:

.. code-block:: python

    from scriptor import Program

    python = Program('python')

    # Run a program (and wait for finish)
    program('myscript.py')

You can also conveniently parametrize programs.
This runs command ``myscript.py --report_date 2022-01-01``:

.. code-block:: python

    program('myscript.py', report_date="2022-01-01")



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
