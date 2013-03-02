Generate nix expressions
========================

Using ``python2nix`` with pip:::

    % pip install python2nix
    % python2nix Plone --eggs Plone --ignore Pillow --output plone.nix

or shorter::

    % python2nix Plone -e Plone -i elementtree -o plone.nix


Using ``python2nix`` with `zc.buildout`_:::

    [plone2nix]
    recipe = python2nix
    eggs = Plone
    output = plone.nix
    ignore =
        Pillow

Above section will generate plone2nix script which will call ``python2nix``
script with arguments defined in that section.


Using generated nix expresions in nixos
=======================================

TODO


.. _`zc.buildout`: http://www.buildout.org/
