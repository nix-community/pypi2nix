pypi2nix - generate Nix expressions for Python packages
=======================================================

``pypi2nix`` is a command line tool that generates `Nix expressions`_ from
different python specific sources (``requirements.txt``, ``buildout.cfg``,
...).

    The only way I can fix bugs with pypi2nix is if you report them. Ping me
    `@garbas`_ if you get stuck.

``pypi2nix`` will (until further notice) only work with latest *unstable*
channel. This is due to ongoing change in python infrastructure happening this
year.

.. contents::


1. Installation
---------------

Make sure Nix is installed.::

    % curl https://nixos.org/nix/install | sh

Next clone `pypi2nix repository`_.::

    % git clone https://github.com/garbas/pypi2nix

And now install it using `nix-env`_ command.::

    % cd pypi2nix
    % nix-env -f release.nix -iA build."x86_64-linux"


2. Usage
--------

The easiest way to generate a Nix expressions is to invoke.::

    % pypi2nix -V "3.5" -e packageA -e packageB==0.1

If you also have ``requirements.txt`` file for you python project you can use
``-r`` option.::


    % pypi2nix -V "3.5" -e packageA -e packageB==0.1 \
        -r requirements.txt -r requirements-dev.txt

If your project relies on ``zc.buildout`` you can give ``-b`` option a try.::

    % pypi2nix -V "2.7" -b buildout.cfg


What is being generated
^^^^^^^^^^^^^^^^^^^^^^^

Option ``-V`` tells pypi2nix which python version to be used. To see which
python versions are available consule ``pypi2nix --help``.

Once Nix expressions are generated you should be able to see 3 new files:

- ``requirements_frozen.txt`` - full frozen set for your for you pypi2nix call.
  This is the output you would expect from `pip freeze`.

- ``requirements.nix`` is a file which contains a nix expression to for the package set that was built.

- ``requirements_override.nix`` - this is an empty file which is ment to
  override generated nix expressions.



Non-python/system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Quite few python package require non-python dependencies to be present at
installation time. For this purpose ``pypi2nix`` has ``-E`` options which can
be used to define this extra non-python dependencies.

``psycopg2`` requires ``pg_config`` binary to be present at installation time::

    % pypi2nix -v -V 2.7 -e psycopg2 -E postgresql

``lxml`` requires ``libxml2`` and ``libxslt`` system package::

    % pypi2nix -v -V 2.7 -e lxml -E libxml2 -E libxslt


Building generated packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build one package::

    % nix-build requirements.nix -A packages.empy

Build all packages::

    % nix-build requirements.nix -A packages

Build python interpreter with all packages loaded::

    % nix-build requirements.nix -A interpreter
    % ./result/bin/python -c "import empy"

Enter developent environemnt::

    % nix-shell requirements.nix -A interpreter
    (nix-shell) % python -c "import empy"


Using generated packages
^^^^^^^^^^^^^^^^^^^^^^^^

If you are working on a project where its dependencies are defined in
``requirements.txt`` then you can create a ``default.nix`` and add generated
packages as buildInputs as demonstrated here::

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

I hope nobody is expecting ``pypi2nix`` to do always a perfect job. In python
packaging there are just too many different cases that we will never be able to
cover. What ``pypi2nix`` tries to do is to get you very close.

When things go not as you expected, ``pypi2nix`` gives you an option to
override anything that it was generated. Even add new packages this way.

An example how you would override a derivation would be adding extra build time
dependencies which we can not detect with ``pypi2nix``. As example lets add
``setuptools-src`` which got generated, but was not detected as build time
dependency of ``execnet``::

    { pkgs, python }:

    self: super: {

      "execnet" = python.overrideDerivation super."execnet" (old: {
        buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
      });

    }


This was you can add or remove any python package.

Including overrides
^^^^^^^^^^^^^^^^^^^

Additional to an autogenerated ``requirements_overrides.nix`` file you
can include preexisting overrides files via the ``-O`` command line
argument.  These overrides will be included the same way as your
``requirements_overrides.nix``.  ``pypi2nix`` allows this via some
common protocols.  The following are some usage examples and
explanations of this feature.

``http`` and ``https``
  ``pypi2nix -V 3 --overrides https://raw.githubusercontent.com/garbas/nixpkgs-python/master/overrides.nix``

  Note that the generated nix expression will check if contents of
  overrides files differs from when a nix expression was build and
  fail of this was the case or the file does not exist anymore.

Local files
  ``pypi2nix -V 3 --override ../some/relative/path --override /some/absolute/path``

Git repositories
  ``pypi2nix -V 3 --override git+https://github.com/garbas/pypi2nix.git#path=overrides.nix``

  If you want to import a file from a specific git repository you have
  to prefix its URL with ``git+``, quite similar to how you would do
  in a ``requirements.txt`` file for ``pip``.

Creating default.nix for you project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nothing speaks better then an example::

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


Important to know here is that you instantiate all generated packages as
``python = import ./requirements.nix { inherit pkgs; };`` which gives you
a python environment with ``pypi2nix`` generated packages and some common
utilities.

To create a package you would use ``python.mkDerivation`` as you are used to
that ``pythonPackages.buildPythonPackage`` function in ``nixpkgs``. All
generated packages are available as one attribute set under
``python.packages``.

.. TODO explain withPackages and show some example

One of future goals of ``pypi2nix`` project is to also improve the UX of our
python tooling in nixpkgs. While this is very hard to do within ``nixpkgs`` it
is almost trivial to experiment with this outside ``nixpkgs``.


Convert generated requirements.nix into nixpkgs overlay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A working example tells more then 1000 words::

    { pkgs ? import <nixpkgs> {}
    }:
    let
      projectOverlay = self: super: {
        customPythonPackages = (import ./requirements.nix { inherit pkgs; }).packages;
      };
    in
      import pkgs.path { overlays = [ projectAOverlay ]; }


3. Existing examples
--------------------

The file `examples/Makefile`_ contains specific instructions for packages like
``sentry``, ``empy``, ``lektor``, ``awscli`` and ``rss2email``.


4. Help developing pypi2nix
---------------------------

Clone `pypi2nix repository`_ and using `nix-shell`_ command enter development
environment.::

    % git clone https://github.com/garbas/pypi2nix
    % cd pypi2nix
    % nix-shell

Code is located in ``src/pypi2nix``.


.. _`Nix expressions`: http://nixos.org/nix/manual/#chap-writing-nix-expressions
.. _`@garbas`: https://twitter.com/garbas
.. _`pypi2nix repository`: https://github.com/garbas/pypi2nix
.. _`examples/Makefile`: https://github.com/garbas/pypi2nix/blob/master/examples/Makefile
.. _`nix-shell`: http://nixos.org/nix/manual/#sec-nix-shell
.. _`nix-env`: http://nixos.org/nix/manual/#sec-nix-env
