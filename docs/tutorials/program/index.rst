.. _program:

Program
=======

This section goes through how Scriptor's program
class works. 

Here is a minimal example of a program:

.. code-block:: python

    >>> from scriptor import Program
    >>> program = Program("python3")
    >>> program(c="print('Hello world')")
    "Hello world"


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   create
   run
   input