Until proper documentation is written let this serve as an example:

1. clone this repository::

    % git clone https://github.com/garbas/pypi2nix
    % cd pypi2nix

2. run nix-shell command and you should have ``pypi2nix`` command working::

   pypi2nix/ % nix-shell
   (nix-shell) pypi2nix/ % which pypi2nix
   /tmp/...-pypi2nix-1.0.0/bin/pypi2nix
   
3. run pypi2nix on some requirements.txt file::

   (nix-shell) pypi2nix/ % echo "empy" > requirements.txt
   (nix-shell) pypi2nix/ % pypi2nix -r requirements.txt
   (nix-shell) pypi2nix/ % ls -la requirements*
   -rw-r--r-- 1 rok users 1064 Feb 17 23:30 requirements_generated.nix
   -rw-r--r-- 1 rok users  311 Feb 17 23:30 requirements.nix
   -rw-r--r-- 1 rok users  148 Feb 17 23:30 requirements_overwrite.nix
   -rw-r--r-- 1 rok users    5 Feb 17 23:29 requirements.txt

4. build your package::

   (nix-shell) pypi2nix/ % nix-build requirements.nix -A empy


Ping me `@garbas`_ if you get stuck.


.. _`@garbas`: https://twitter.com/garbas
