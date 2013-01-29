


Create Plone nix expressions::

   $ python2.7 bootstrap.py -d -c plone.cfg
   $ bin/buildout -N -c plone.cfg
   $ bin/eggdeps Plone -nst | bin/python python2nix.py > plone.nix
