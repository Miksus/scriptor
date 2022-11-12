.. _program-run:

Running Program
================

We use the current interpreter
as our example program:

.. code-block:: python

    import sys
    from scriptor import Program
    python = Program(sys.executable)

To run the program, just call it:

.. code-block:: python

    python('myscript.py')

Note that we passed one positional argument 
to the program (Python interpreter). Read more
about :ref:`program parameters <program-input>`. 

You can also run the program async:

.. code-block:: python

    await python.call_async('myscript.py')

Outputs
-------

Typically programs put their outputs to the standard 
output (stdout). Because of this, Scriptor returns 
the stdout as the output of the call.

For example, we have this script called ``myscript.py``:

.. code-block:: python

    print("Hello")
    print("world")

Then if we run this program:

.. code-block:: python

    >>> python('myscript.py')
    'Hello\nworld'

Bytes as Output
^^^^^^^^^^^^^^^

Note that the output is string by default. You can also
return raw bytes by setting the ``output_type``:

.. code-block:: python

    >>> python = Program('python', output_type='bytes')
    >>> python('myscript.py')
    b'Hello\nworld\n'

Custom Output
^^^^^^^^^^^^^

Moreover, you can also add your own output parser if for 
example your program returns an object you wish to parse.

For example, let's say you have a program that returns 
a JSON in the stdout. Let's call it ``myscript.py``:

.. code-block:: python

    print('{"name":"Miksu", "age":25, "life":null}')

Then we set a custom output parser:

.. code-block:: python

    >>> import json
    >>> python = Program('python', output_parser=json.loads)
    >>> python('myscript.py')
    {"name": "Miksu", "age": 25, "life": None}

Errors
------

Standard error (stderr) is the typical output 
for the error messages if the program fails.
Scriptor conveniently puts the stderr to the 
exception.

We have a Python script called ``failing.py``
which looks like:

.. code-block:: python

    raise RuntimeError("Oops")

If we run this program using Scriptor:

.. code-block:: python

    output = python('failing_script.py')

we get an error that looks like this:

.. code-block::

    Traceback (most recent call last):
    File "...", line ..., in <module>
        python("failing_script.py")
    ...
    File "...\scriptor\process.py", line ..., in _raise_for_error
        raise ProcessError(
    scriptor.process.ProcessError: Traceback (most recent call last):
    File "failing_script.py", line 1, in <module>
        raise RuntimeError("Oops!")
    RuntimeError: Oops!

.. note::

    The exception class is ``scriptor.ProcessError`` and not ``RuntimeError``.

Starting a Program
------------------

You can also start a program and handle the 
finish later. Scriptor provides further 
abstraction for ``subprocess.Popen`` and
``asyncio.subprocess.Process`` to make 
working with the processes more intuitive.

To start a process synchronously:

.. code-block:: python

    process = python.start('myscript.py')

To start a process with async:

.. code-block:: python

    process = await python.start_async('myscript.py')
