pypi2nix - generate Nix expressions for Python packages
=======================================================

``pypi2nix`` is a command line tool that generates `Nix expressions`_ from
different ``requirements.txt``. This is useful for:

- Building a Nix derivation for a program written in Python as part of
  packaging it.

- Setting up a development environment to hack on a program written in Python.

    The only way we can fix bugs with pypi2nix is if you report them. Please
    create an issue if you discover problems.

``pypi2nix`` will (until further notice) only work with latest *unstable*
channel. This is due to ongoing changes in Python infrastructure happening in
Nixpkgs.

The `Nixpkgs manual section about Python
<https://nixos.org/nixpkgs/manual/#python>`_ makes good reading if you
haven't seen it already.

.. contents::


1. Installation
---------------

``pypi2nix`` is part of ``nixpkgs``.  If you just want to use
``pypi2nix`` on your system, it is recommended that you install it via
the regular means, e.g. ``nix-env -iA nixos.pypi2nix`` on NixOS or
``nix-env -iA nixpkgs.pypi2nix`` on other systems utilizing nix.

System Requirements
^^^^^^^^^^^^^^^^^^^

Make sure Nix is installed::

    % curl https://nixos.org/nix/install | sh

Currently ``pypi2nix`` is only tested against ``linux`` systems.
Supported ``nixpkgs`` channels are ``nixos-19.09`` and
``nixos-unstable``.  Due to the nature of ``nixos-unstable`` the
occasional breakage of ``pypi2nix`` is to be expected.  We try to
provide fixes in that regard in a timely manner.


Ad hoc Installation (Simple)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For just installing the package with a command, use `nix-env`_::

  nix-env -if https://github.com/nix-community/pypi2nix/tarball/master

Declarative Installation (Advanced)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer to explicitly declare each installed package in your
Nix(OS) or project configuration, you can do the following:

First, import the package from its ``default.nix`` by fetching the
whole git repository with ``pkgs.fetchgit``.  Afterwards you can just
add the imported attribute the list of installed software.

Below you find an example for NixOS' ``configuration.nix``. Other
methods like `home-manager`_ work similar::

    let
      pypi2nix = import (pkgs.fetchgit {
        url = "https://github.com/nix-community/pypi2nix";
        # adjust rev and sha256 to desired version
        rev = "v2.0.1";
        sha256 = "sha256:0mxh3x8bck3axdfi9vh9mz1m3zvmzqkcgy6gxp8f9hhs6qg5146y";
      }) {};
    in
      environment.systemPackages = [
        # your other packages
        pypi2nix
      ];



2. Usage
--------

The easiest way to generate a Nix expressions is to invoke::

    % pypi2nix -e packageA -e packageB==0.1

If you also have a ``requirements.txt`` file for your Python project you can use
the ``-r`` option.

::

    % pypi2nix -e packageA -e packageB==0.1 \
        -r requirements.txt -r requirements-dev.txt


What is being generated
^^^^^^^^^^^^^^^^^^^^^^^

Option ``-V`` tells pypi2nix which python version to be used. To see which
Python versions are available consult ``pypi2nix --help``.

Once Nix expressions are generated you should be able to see 3 new files:

- ``requirements_frozen.txt`` - full frozen set for your for your pypi2nix call.
  This is the output you would expect from ``pip freeze``.

- ``requirements.nix`` is a file which contains a nix expression to for the package set that was built.

- ``requirements_override.nix`` - this is an empty file which lets you
  override generated nix expressions.


Building generated packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build one package::

    % nix build -f requirements.nix packages.empy

Build all packages::

    % nix build -f requirements.nix packages

Build python interpreter with all packages loaded::

    % nix build -f requirements.nix interpreter
    % ./result/bin/python -c "import empy"

Enter development environment::

    % nix run -f requirements.nix interpreter
    [user@localhost:~/dev/nixos/pypi2nix) % python -c "import empy"


Using generated packages
^^^^^^^^^^^^^^^^^^^^^^^^

If you are working on a project where its dependencies are defined in
``requirements.txt`` then you can create a ``default.nix`` and add generated
packages as ``buildInputs``, as demonstrated here::

    {}:
    let
      python = import ./requirements.nix { inherit pkgs; };
    in python.mkDerivation {
      name = "ProjectA-1.0.0";
      src = ./.;
      buildInputs = [
        python.packages."coverage"
        python.packages."flake8"
        python.packages."mock"
        python.packages."pytest"
        python.packages."pytest-asyncio"
        python.packages."pytest-cov"
        python.packages."pytest-mock"
        python.packages."pytest-xdist"
        python.packages."virtualenv"
      ];
      propagatedBuildInputs = [
        python.packages."aiohttp"
        python.packages."arrow"
        python.packages."defusedxml"
        python.packages."frozendict"
        python.packages."jsonschema"
        python.packages."taskcluster"
        python.packages."virtualenv"
      ];
      ...
    }


As you can see you can access all packages via ``python.packages."<name>"``. If
you want to depend on *all* packages you can even do::


    propagatedBuildInputs = builtins.attrValues python.packages;

Command line options
^^^^^^^^^^^^^^^^^^^^

``-v``
    Increase amount and detail of information output to the user.
    Verbosity levels are ``ERROR``, ``WARNING``, ``INFO`` and
    ``DEBUG`` in that order.  The default verbosity is ``INFO``.

``-q``
    Reduce amount and detail of information output to the user.  See
    ``-v`` for more information.

``-I/--nix-path TEXT``
    Add entries to the ``NIX_PATH`` environment variable similarly to
    how ``-I`` works with ``nix`` executables like ``nix-build``.
    This can be useful for generating package sets based on a
    different ``nixpkgs`` version than the one used one the local
    system.

``--nix-shell PATH``
    Path to an alternative version of the ``nix-shell`` command.  The
    default is the first executable that will be found in the current
    ``PATH`` of the system.

``--version``
    Show the current version of ``pypi2nix``

``--basename TEXT``
    This option determins the name the produced files.  So with
    ``--basename environment`` you would get the files
    ``environment.nix``, ``environment_frozen.nix`` and
    ``environment_override.nix``.

``--extra-build-inputs/-E TEXT``
    Extra build inputs that the required python packages need to run,
    e.g. ``libffi`` or ``libgl``.  In that case you would provide ``-E
    "libffi libgl"``.  These nix packages will be available in the
    build environment for the wheels.

``--emit-extra-build-inputs/--no-emit-extra-build-inputs``
    These options let you control if external build dependencies
    specified via ``-E`` will end up in the generated nix package set.
    Please note that if you select this option, your overrides need to
    make sure that python packages find their respective external
    dependencies.

``--extra-env/-N TEXT``
    Extra environment variables that will be passed to the build
    environment.  Note that you can use nix expressions in this
    string, e.g. ``-N 'BERKELEYDB_DIR=${pkgs.db.dev}'``.

``--enable-tests/-T``
    Specify this flag if you want to enable the check phase of all
    packages in the generated nix expression.  Please note that this
    feature is highly exprimental and will probably not work for your
    use case.

``--python-version/-V``
    Specify the python version you want the requirement set to be
    built with.  The default is ``3`` which translates to the
    ``python3`` derivation of ``nixpkgs``.

``--requirements/-r FILE``
    Specify a requirements file, similar as you would with ``pip``.
    ``pypi2nix`` tries to be fully compatible with the file format of
    ``pip``.

``--editable/-e TEXT``
    This option allows you to specify individual requirements that get
    added to the requirement set, e.g. ``pypi2nix -e attrs``,
    ``pypi2nix -e $HOME/src/myproject#egg=myproject`` or ``pypi2nix -e .#egg=myegg``.

``--setup-requires/-s TEXT``
    Allows you to specify python packages that need to be present in
    the build environment of other packages, a good example of this
    would be ``setuptools-scm``.  Note that ``pypi2nix`` tries to
    detect these dependencies on its own.  You only need to specify
    this flag in cases where a package author or maintainer forgot to
    mention build time dependencies in their setup or neither
    ``setup.cfg`` nor ``pyproject.toml`` is used.

``--overrides/-O URL``
    Allows you to specify additional overrides that conform to the
    general structure of ``requirements_override.nix``.  We support
    regular URLs with ``http`` and ``https`` scheme and also ``git``.
    An example for using ``https`` would be ``pypi2nix -O
    https://myoverrides.test/overrides.nix``.  Reusing an overlay from
    a git repository would be done like so: ``pypi2nix -O
    git+https://github.com/nix-community/pypi2nix.git&path=requirement_override.nix``.
    Please keep in mind that these overrides are incorporated in a nix
    expression with a precalculated hash value.  So if the file
    changes upstream your generated package can not be built anymore.

``--default-overrides/--no-default-overrides``
    Pull in overrides from
    ``https://github.com/nix-community/pypi2nix-overrides``.  This
    feature is enabled by default.

``--wheels-cache/-W TEXT``
    A location where prebuilt wheels can be found.  This option will
    ultimately be passed to ``pip --find-links``.  Only point to
    wheels that are built through ``pypi2nix`` on your own or a very
    similar system.

``--build-directory TEXT``
    **Warning** A bug in ``pypi2nix`` currently prevents some packages
    from being built with this option set.  It is recommended to not
    use this flag.

    The directory where pypi2nix would build the python environment to
    generate the desired nix expression.  If not specified, the build
    directory will be temporary and is deleted before the program
    exits.


3. When it doesn't work
-----------------------

I hope nobody is expecting ``pypi2nix`` to do always a perfect job. In Python
packaging, there are just too many different cases that we will never be able to
cover. What ``pypi2nix`` tries to do is to get you very close.

Sometimes ``pypi2nix`` fails entirely. If this happens, open a bug --
it's almost always a bug in ``pypi2nix``. However, sometimes
``pypi2nix`` succeeds but the resulting ``requirements.nix`` file
fails during the building of your Python package. Depending on what
the problem is, this section may be helpful.

Non-Python/system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Quite a few Python packages require non-Python dependencies to be
present at build time. These packages will fail to build with error
messages about not being able to find ``foo.h`` or some ``fooconfig``
file. To work around this, ``pypi2nix`` has ``-E`` options which can
be used to include extra non-Python dependencies.

For example, ``psycopg2`` requires ``pg_config`` binary to be present at installation time::

    % pypi2nix -v -V 2.7 -e psycopg2 -E postgresql

``lxml`` requires ``libxml2`` and ``libxslt`` system package::

    % pypi2nix -v -V 2.7 -e lxml -E libxml2 -E libxslt


Additional environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some packages expect additional environment variables to be set::

  % pypi2nix -v -V 2.7 -e bsddb3 -N 'BERKELEYDB_DIR=${pkgs.db.dev}'


Using requirements_override.nix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some other failures might be caused because the derivation that
``pypi2nix`` wrote was incomplete. A very common situation is that
``pypi2nix`` didn't include all the dependencies of some package. As
an example, ``execnet`` depends on ``setuptools-scm``, but
``pypi2nix`` may not detect this.

When this happens, Nix will fail to build ``execnet``, perhaps with an
error message from distutils/setuptools complaining that it can't find
a distribution for ``setuptools-scm``. What's happening here is that
normally ``execnet`` would fetch ``setuptools-scm`` from PyPI, but Nix
disables network access to guarantee reproducability. So when you
build ``execnet``, it fails to find ``setuptools-scm``.

For these situations, ``pypi2nix`` provides a
``requirements_override.nix`` file, which lets you override anything
that it generated. You can even add new packages to the dependency set
this way.

As an example, let's add ``setuptools-scm`` as a build-time dependency
of ``execnet``. Here's the ``requirements_override.nix``::

    { pkgs, python }:

    self: super: {

      "execnet" = python.overrideDerivation super."execnet" (old: {
        buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
      });

    }


In a similar way, you can add or remove any Python package.

Shared overrides
^^^^^^^^^^^^^^^^

In addition to the empty autogenerated ``requirements_overrides.nix``
file, you can include pre-existing overrides files.  These overrides
will be included the same way as your ``requirements_overrides.nix``.

The ``pypi2nix`` author also maintains a set of "default" overrides at
https://github.com/nix-community/pypi2nix-overrides/blob/master/overrides.nix --
you can include these by using the ``--default-overrides`` argument to
``pypi2nix``. These overrides are designed in such a way that they
only override dependencies that were already present in your
``requirements.nix``.

You can also include an overrides file using the ``-O`` command line
argument.  ``pypi2nix`` can fetch these overrides from a local file or
over certain common protocols.

``http`` and ``https``
  ``pypi2nix -V 3 --overrides https://raw.githubusercontent.com/nix-community/pypi2nix-overrides/master/overrides.nix``

  Note that the generated Nix expression will check if contents of
  the overrides file differs from when the Nix expression was built, and
  fail if this was the case (or the file does not exist anymore).

Local files
  ``pypi2nix -V 3 --override ../some/relative/path --override /some/absolute/path``

Git repositories
  ``pypi2nix -V 3 --override git+https://github.com/nix-community/pypi2nix.git#path=overrides.nix``

  If you want to import a file from a specific git repository you have
  to prefix its URL with ``git+``, quite similar to how you would do
  in a ``requirements.txt`` file for ``pip``.

4. Advanced Use
---------------

Creating default.nix for your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nothing speaks better than an example::

    { }:

    let
      pkgs = import <nixpkgs> {};
      python = import ./requirements.nix { inherit pkgs; };
    in python.mkDerivation {
      name = "projectA-1.0.0";
      src = ./.;
      buildInputs = [
        python.packages."coverage"
        python.packages."flake8"
        python.packages."mock"
        python.packages."pytest"
        python.packages."pytest-asyncio"
        python.packages."pytest-cov"
        python.packages."pytest-mock"
        python.packages."pytest-xdist"
      ];
      propagatedBuildInputs = [
        python.packages."aiohttp"
        python.packages."arrow"
        python.packages."defusedxml"
        python.packages."frozendict"
        python.packages."jsonschema"
      ];
      checkPhase = ''
        export NO_TESTS_OVER_WIRE=1
        export PYTHONDONTWRITEBYTECODE=1

        flake8 src/
        py.test --cov=src -cov-report term-missing
        coverage html
      '';
    }


Important to know here is that you instantiate all generated packages
as ``python = import ./requirements.nix { inherit pkgs; };`` which
gives you a Python environment with all the packages generated by
``pypi2nix`` as well as some common utilities.

To create a package you use ``python.mkDerivation`` which works like
the ``pythonPackages.buildPythonPackage`` function in ``nixpkgs``. All
generated packages are available as one attribute set under
``python.packages``.

.. TODO explain withPackages and show some example

One of future goals of ``pypi2nix`` project is to also improve the UX of our
Python tooling in nixpkgs. While this is very hard to do within ``nixpkgs`` it
is almost trivial to experiment with this outside ``nixpkgs``.


Convert generated requirements.nix into nixpkgs overlay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A working example is worth 1000 words.

overlay.nix::

    self: super:
    {
      customPython =
          (import ./requirements.nix { pkgs = self; });
    }

shell.nix::

    with (import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; });
    customPython.interpreter


5. Help developing pypi2nix
---------------------------

Clone `pypi2nix repository`_ and using ``nix-shell`` command enter development
environment.::

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
directory in the users ``PATH`` if they choose to enter ``nix-shell`` in
the top level directory of this project.

Version bumping
^^^^^^^^^^^^^^^

We use ``bumpv`` to manage the current version of this project.  This
program should be part of the development environment.


.. _`Nix expressions`: http://nixos.org/nix/manual/#chap-writing-nix-expressions
.. _`pypi2nix repository`: https://github.com/nix-community/pypi2nix
.. _`examples/Makefile`: https://github.com/nix-community/pypi2nix/blob/master/examples/Makefile
.. _`nix-env`: http://nixos.org/nix/manual/#sec-nix-env
.. _`pytest`: https://pytest.org
.. _`home-manager`: https://github.com/rycee/home-manager
