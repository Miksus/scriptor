.. _cookbook-git:

Git
===

This is an example of how to use Git with
Scriptor.

Functional
----------

First we go through how to use Git functionally
with Scriptor.

First we create a Git program:

.. code-block:: python

    from scriptor import Program
    git = Program('git')

As git works on the current working directory (cwd),
we need to change that to our repository:

.. code-block:: python

    myrepo = git.use(cwd="path/to/myrepo")

.. note::

    Method ``.use`` copies the program.
    You can create programs for multiple 
    repositories by:

    .. code-block:: python

        repo_scriptor = git.use(cwd="/repos/scriptor")
        repo_redmail = git.use(cwd="/repos/redmail")

Then we can use this:

.. code-block:: python

    >>> myrepo("status")
    """On branch main
    nothing to commit, working tree clean"""

    >>> myrepo("fetch")
    >>> myrepo("log", n=2)
    """commit 7939dde2fef44369f72911de17188dd51bbfd2e5
    Author: Mikael Koli <mikael.koli@example.com>
    Date:   Sat Nov 12 12:33:09 2022 +0200

        Made the thing work.

    commit 492f63918d750c794641f90fb4b5440c4195e17b
    Author: Mikael Koli <mikael.koli@example.com>
    Date:   Sat Nov 12 11:53:18 2022 +0200

        Broke the thing."""


Object Oriented
---------------

You can also create more abstraction by subclassing
``BaseProgram``:

.. code-block:: python

    from scriptor import BaseProgram
    
    class Git(BaseProgram):

        program = "git"

        def __init__(self, repo=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if repo:
                self.cwd = repo

        def fetch(self):
            "Run: git fetch"
            return self("fetch")

        @property
        def status(self):
            return self("status")

        def log(self, n:int):
            return self("log", n=n)
        ...


Then to use this:

.. code-block:: python

    >>> git = Git("path/to/myrepo")
    >>> git.status
    """On branch main
    nothing to commit, working tree clean"""

    >>> git.fetch()
    >>> git.log(n=2)
    """commit 7939dde2fef44369f72911de17188dd51bbfd2e5
    Author: Mikael Koli <mikael.koli@example.com>
    Date:   Sat Nov 12 12:33:09 2022 +0200

        Made the thing work.

    commit 492f63918d750c794641f90fb4b5440c4195e17b
    Author: Mikael Koli <mikael.koli@example.com>
    Date:   Sat Nov 12 11:53:18 2022 +0200

        Broke the thing."""