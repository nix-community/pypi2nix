pypi2nix - generates nix expressions for PyPI packages
======================================================


0. Ensure that Nix is installed and confiured properly
------------------------------------------------------

To install nix you can simple do::

    curl https://nixos.org/nix/install | sh


1. Clone the repository
-----------------------

::

    git clone https://github.com/garbas/pypi2nix cd pypi2nix


2. Inside the directory, run the ``nix-shell`` command
------------------------------------------------------

::

    nix-shell

Now, the ``pypi2nix`` command should be available. To check this is the case,
you can run ``which pypi2nix``.


3. Add the name of your package to a text file, e.g.

::

    echo "empy" > requirements.txt

Alternatively, you can also try a URL like

::

    echo "https://github.com/wking/rss2email/archive/master.zip" > requirements.txt


4. Run the ``pypi2nix`` command
-------------------------------

::

        pypi2nix -r requirements.txt -V "2.7"

   If your package requires a different version of Python, you can use the
   ``-V`` option. For example, ::

        pypi2nix -r requirements.txt -V "3.4"

   If your project requires some system libraries you can use the ``-E``
   option. For example, ::

        pypi2nix -r requirements.txt -V "3.4" -E "libxslt libxml2"

   Pypi2nix will now generate a file ``requirements.nix``.

5. Build your package via
-------------------------

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


Examples
--------

The file ``examples/Makefile`` contains specific instructions for packages like
``sentry``, ``empy``, ``lektor``, ``awscli`` and ``rss2email``.


Ping me `@garbas`_ if you get stuck.


.. _`@garbas`: https://twitter.com/garbas
.. _`manual`: http://nixos.org/nix/manual/#name-14
