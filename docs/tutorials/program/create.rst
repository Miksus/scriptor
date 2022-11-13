Creating Program
================

There are two ways to create a program.
The simplest one is to just create one 
from the ``Program`` class:

.. code-block:: python

    from scriptor import Program
    git = Program('git')

Alternatively you can subclass ``BaseProgram``
if you want to make an interface for your 
program, ie.:

.. code-block:: python

    from scriptor import BaseProgram

    class Git(BaseProgram):

        program = 'git'

        def fetch(self):
            "Run command: git fetch"
            return self('fetch')

        def log(self, n):
            "Run command: git log -n ..."
            return self('log', n=n)

Then to create a program instance:

.. code-block:: python

    git = Git()

Changing Settings
-----------------

Often it is desired to have specific settings 
for running a program. For example, you may 
want to run a program with a different current 
working directory (cwd) than where the current 
program is.

Here is an example:

.. code-block:: python

    >>> repo_1 = git.use(cwd="path/to/repo_1")
    >>> repo_2 = git.use(cwd="path/to/repo_2")

    >>> # Run git status with repo_1 as CWD
    >>> repo_1("status")
    ...

.. note::

    Method ``program.use(...)`` copies the instance
    thus you can easily create copies to run programs
    in different directories or settings.

Settings
--------

.. glossary::

    cwd
        Current working directory used for running the program.
        By default same as current.

    timeout
        Number of seconds to wait before terminating the program
        due to timeout. By default None.

    arg_form: ``'long'``, ``'short'`` or ``None``
        Form of the argument, either ``long`` or ``short``. 
        If ``None``, the argument form is interpret from the length 
        of the key. By default None.

    default_kwargs: Dict
        Default keyword arguments to pass all calls.

    output_type: ``'str'`` or ``'bytes'``
        Type of the program output (stdout), either ``'str'`` or 
        ``'bytes'``. By default ``'str'``.

    output_parser: callable
        Output parser. By default None.
    
    env: dict
        Additional environment variables to pass to the program in addition
        to the current. Overrides the ones that already exists. By default 
        empty dict.

    include_current_env: bool
        Whether to include current environment variables. If you want to 
        set all manually, set this to False and pass the environment 
        variables via ``env``. By default True.

.. note::

    By default, Scriptor does not use shell to avoid command injection.