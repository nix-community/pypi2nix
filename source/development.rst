Help developing pypi2nix
------------------------

Clone `pypi2nix repository`_ and using the ``nix-shell`` command enter
development environment.::

    % git clone https://github.com/nix-community/pypi2nix
    % cd pypi2nix
    % nix-shell

Code is located in ``src/pypi2nix``.

Testing
^^^^^^^

Pypi2nix comes with two kinds of tests: unit tests and integration
tests.  They can be found in the folders ``/unittests`` and
``/integrationtests`` respectively.

Unit tests are straight forward.  They are run via `pytest`_ and (try
to) follow `pytest`_ best practices.  Idealy all of pypi2nix's code
should be covered by unittests.  If possible unittests should not go
online and fetch data from the internet.  If this cannot be avoided
use the ``@nix`` decorator, found in ``unittests.switches`` to mark
tests that require network access.

Integration tests
"""""""""""""""""

Integration tests are a little bit more involved.  We implemented a
small framework to write new tests and maintain old ones.  Check out
``integrationtests.framework`` for information on how to write custom
integration tests.  To run all integration tests run
``run_integration_tests.py`` from the ``scripts`` directory.  If you
use ``nix-shell`` to create your development environment then the
``scripts`` directory should be in you ``PATH`` variable.

Please note that all integration test cases are classes deriving from
``integrationtests.framework.IntegrationTest``.  Also all these tests
must end with ``TestCase``, e.g. ``MyCustomTestCase``.

Maintainance scripts
^^^^^^^^^^^^^^^^^^^^

The ``scripts`` folder contains programs that help to maintain the
repository.  We expect the user to have all the packages from the
build environment of pypi2nix installed.  We register the ``scripts``
directory in the users ``PATH`` if they choose to enter ``nix-shell``
in the top level directory of this project.  All maintainance scripts
should offer a list of legal command line arguments via the ``--help``
flag.

Version bumping
^^^^^^^^^^^^^^^

We use ``bumpv`` to manage the current version of this project.  This
program should be part of the development environment.

Code formatting
^^^^^^^^^^^^^^^

We try to automate as much code formatting as possible.  For python
source code we use ``black`` and ``isort``.  For nix source code we
use ``nixfmt``.  Both tools are available in development environment
provided by ``nix-shell``.  The continous integration system will
complain if the code is not formatted properly and the package won't
build.  You can automatically format all code via the
``format_sources.py`` program.  You can run it like any other
maintainance script from any working directory you like as long as you
are inside the provided ``nix-shell`` environment. Example::

    [nix-shell:~/src/pypi2nix]$ format_sources.py
    Skipped 2 files
    All done! ✨ 🍰 ✨
    131 files left unchanged.
    Success: no issues found in 47 source files
    Success: no issues found in 122 source files


.. _`pytest`: https://pytest.org
.. _`pypi2nix repository`: https://github.com/nix-community/pypi2nix
