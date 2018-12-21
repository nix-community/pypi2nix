pypi2nix - generate Nix expressions for Python packages
=======================================================

``pypi2nix`` is a command line tool that generates `Nix expressions`_ from
different python specific sources (``requirements.txt``, ``buildout.cfg``,
\...). This is useful for:

- Building a Nix derivation for a program written in Python as part of
  packaging it.

- Setting up a development environment to hack on a program written in Python.

    The only way we can fix bugs with pypi2nix is if you report them. Please
    create an issue if you discover problems.

``pypi2nix`` will (until further notice) only work with latest *unstable*
channel. This is due to ongoing changes in python infrastructure happening in
nixpkgs.

.. contents::


1. Installation
---------------

Make sure Nix is installed.::

    % curl https://nixos.org/nix/install | sh

And now install it using `nix-env`_ command.::

    % nix-env -if https://github.com/garbas/pypi2nix/tarball/master


2. Usage
--------

The easiest way to generate a Nix expressions is to invoke.::

    % pypi2nix -V "3.5" -e packageA -e packageB==0.1

If you also have a ``requirements.txt`` file for your Python project you can use
the ``-r`` option.::


    % pypi2nix -V "3.5" -e packageA -e packageB==0.1 \
        -r requirements.txt -r requirements-dev.txt

If your project relies on ``zc.buildout`` you can give ``-b`` option a try.::

    % pypi2nix -V "2.7" -b buildout.cfg


What is being generated
^^^^^^^^^^^^^^^^^^^^^^^

Option ``-V`` tells pypi2nix which python version to be used. To see which
Python versions are available consult ``pypi2nix --help``.

Once Nix expressions are generated you should be able to see 3 new files:

- ``requirements_frozen.txt`` - full frozen set for your for your pypi2nix call.
  This is the output you would expect from `pip freeze`.

- ``requirements.nix`` is a file which contains a nix expression to for the package set that was built.

- ``requirements_override.nix`` - this is an empty file which lets you
  override generated nix expressions.



Non-Python/system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Quite a few Python packages require non-Python dependencies to be
present at build time. If these packages are missing,
``pypi2nix`` may succeed, but the resulting `requirements.nix` file
will fail during the building of your Python package.

To work around this, ``pypi2nix`` has ``-E`` options which can
be used to include extra non-Python dependencies.

For example, ``psycopg2`` requires ``pg_config`` binary to be present at installation time::

    % pypi2nix -v -V 2.7 -e psycopg2 -E postgresql

``lxml`` requires ``libxml2`` and ``libxslt`` system package::

    % pypi2nix -v -V 2.7 -e lxml -E libxml2 -E libxslt


Additional environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some packages expect additional environment variables to be set::

  % pypi2nix -v -V 2.7 -e bsddb3 -N 'BERKELEYDB_DIR=${pkgs.db.dev}'


Building generated packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build one package::

    % nix build -f requirements.nix packages.empy

Build all packages::

    % nix build -f requirements.nix packages

Build python interpreter with all packages loaded::

    % nix build -f requirements.nix interpreter
    % ./result/bin/python -c "import empy"

Enter developent environemnt::

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
you want to depend on *all* packages you can as well do::


    propagatedBuildInputs = builtins.attrValues python.packages;



Using requirements_override.nix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I hope nobody is expecting ``pypi2nix`` to do always a perfect job. In Python
packaging, there are just too many different cases that we will never be able to
cover. What ``pypi2nix`` tries to do is to get you very close.

When things go not as you expected, ``pypi2nix`` gives you an option to
override anything that it was generated. You can even add new packages this way.

An example of how you would override a derivation would be adding extra build time
dependencies which ``pypi2nix`` did not detect. As an example, let's add
``setuptools-scm`` which got generated, but was not detected as a build time
dependency of ``execnet``::

    { pkgs, python }:

    self: super: {

      "execnet" = python.overrideDerivation super."execnet" (old: {
        buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
      });

    }


In a similar way, you can add or remove any Python package.

Shared overrides
^^^^^^^^^^^^^^^^

In addition to an autogenerated ``requirements_overrides.nix`` file,
you can include pre-existing overrides files.  These overrides will be
included the same way as your ``requirements_overrides.nix``.

The ``pypi2nix`` author also maintains a set of "default" overrides at
https://github.com/garbas/nixpkgs-python/blob/master/overrides.nix --
you can include these by using the ``--default-overrides`` argument to
``pypi2nix``. These overrides are designed in such a way that they
only override dependencies that were already present in your
``requirements.nix``.

You can also include an overrides file using the ``-O`` command line
argument.  ``pypi2nix`` can fetch these overrides from a local file or
over certain common protocols::

``http`` and ``https``
  ``pypi2nix -V 3 --overrides https://raw.githubusercontent.com/garbas/nixpkgs-python/master/overrides.nix``

  Note that the generated Nix expression will check if contents of
  the overrides file differs from when the Nix expression was built, and
  fail if this was the case (or the file does not exist anymore).

Local files
  ``pypi2nix -V 3 --override ../some/relative/path --override /some/absolute/path``

Git repositories
  ``pypi2nix -V 3 --override git+https://github.com/garbas/pypi2nix.git#path=overrides.nix``

  If you want to import a file from a specific git repository you have
  to prefix its URL with ``git+``, quite similar to how you would do
  in a ``requirements.txt`` file for ``pip``.

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


3. Existing examples
--------------------

The file `examples/Makefile`_ contains demonstrations using packages like
``sentry``, ``empy``, ``lektor``, ``awscli`` and ``rss2email``.


4. Help developing pypi2nix
---------------------------

Clone `pypi2nix repository`_ and using ``nix run`` command enter development
environment.::

    % git clone https://github.com/garbas/pypi2nix
    % cd pypi2nix
    % nix run -f .

Code is located in ``src/pypi2nix``.


.. _`Nix expressions`: http://nixos.org/nix/manual/#chap-writing-nix-expressions
.. _`pypi2nix repository`: https://github.com/garbas/pypi2nix
.. _`examples/Makefile`: https://github.com/garbas/pypi2nix/blob/master/examples/Makefile
.. _`nix-env`: http://nixos.org/nix/manual/#sec-nix-env
