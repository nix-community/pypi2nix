pypi2nix - generates nix expressions for PyPI packages
======================================================

``pypi2nix`` is a command line tool that generates `Nix expressions`_ from
different python specific sources.

TODO: report bugs

Ping me `@garbas`_ if you get stuck.

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

What is being generated
^^^^^^^^^^^^^^^^^^^^^^^

Option ``-V`` tells pypi2nix which python version to be used. To see which
python versions are available consule ``pypi2nix --help``.

Once Nix expressions are generated you should be able to see 3 new files:

- ``requirements_generated.nix`` - this are the generated nix expressions

- ``requirements_override.nix`` - this is an empty file which is ment to
  override generated nix expressions.

- ``requirements.nix`` is a file which connects ``requirements_generated.nix``
  and ``requirements_override.nix`` and exposes it for futher usage.

Building generated packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build one package::

    % nix-build requirements.nix -A pkgs.empy

Build all packages::

    % nix-build requirements.nix -A pkgs

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
        python.pkgs."coverage"
        python.pkgs."flake8"
        python.pkgs."mock"
        python.pkgs."pytest"
        python.pkgs."pytest-asyncio"
        python.pkgs."pytest-cov"
        python.pkgs."pytest-mock"
        python.pkgs."pytest-xdist"
        python.pkgs."virtualenv"
      ];
      propagatedBuildInputs = [
        python.pkgs."aiohttp"
        python.pkgs."arrow"
        python.pkgs."defusedxml"
        python.pkgs."frozendict"
        python.pkgs."jsonschema"
        python.pkgs."taskcluster"
        python.pkgs."virtualenv"
      ] ++ (builtins.attrValues python.modules);
      ...
    }
    

As you can see you can access all packages via ``python.pkgs."<name>"``. If you
want to depend on *all* packages you can as well do::


    propagatedBuildInputs = builtins.attrValues python.pkgs;



.. TODO: how to override packages
.. TODO: how to create default.nix


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
