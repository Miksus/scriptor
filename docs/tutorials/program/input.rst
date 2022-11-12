.. _program-input:

Program Parameters
==================

Typically programs take in parameters or data in 
the following forms:

- Positional arguments
- Keyword arguments (either short or long form)
- Standard input (stdin)

Positional Arguments
--------------------

.. code-block:: python

    python("myscript.py", "positional_argument")

Keyword Arguments
-----------------

Calling a program supports also keyword arguments.
The most common way to pass keyword arguments to 
programs is to supply them either in short form
(ie. ``-o myfile.txt``) or long form (ie. 
``--output myfile.txt``). 

Scriptor supports both forms and it guesses the form 
by the length of the argument name. If it is shorter than
what is specified in the argument ``long_form_threshold``,
the argument will be passed in short form. If it is longer,
it is passed as long form. This is ``3`` by default.

The below will run command: ``python myscript.py --report_date 2022-11-11``

.. code-block:: python

    python("myscript.py", report_date="2022-11-11")


The below will run command: ``python myscript.py -rd 2022-11-11``

.. code-block:: python

    python("myscript.py", rd="2022-11-11")

Standard Input (stdin)
----------------------

.. code-block:: python

    from scriptor.program import Input

    python("myscript.py", Input('some data'))

.. warning::

    You should pass only one ``Input`` per call.

.. note::

    You can have positional arguments as well.
    You can pass those before or after the standard
    input.

    These are identical:

    .. code-block:: python

        python("myscript.py", Input('some data'), "myarg")
        python("myscript.py", "myarg", Input('some data'))