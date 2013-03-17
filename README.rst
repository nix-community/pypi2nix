Generate nix expressions
========================

Using ``pypi2nix`` with pip:::

    % pip install pypi2nix
    % pypi2nix Plone --dists Plone --ignore Pillow --output plone.nix

or shorter::

    % pypi2nix Plone -d Plone -i elementtree -o plone.nix


Using ``pypi2nix`` with `zc.buildout`_:::

    [plone2nix]
    recipe = pypi2nix
    eggs = Plone
    output = plone.nix
    ignores =
        Pillow

Above section will generate plone2nix script which will call ``pypi2nix``
script with arguments defined in that section.


Using generated nix expresions in nixos
=======================================

TODO


.. _`zc.buildout`: http://www.buildout.org/
