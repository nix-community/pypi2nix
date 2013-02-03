
Create Plone nix expressions from an existing plone instance::

   $ ./bin/buildout annotate | sed '1,/\[versions\]/d' | grep = | sed 's#=##' > plonedeps
   $ bin/python plone2nix.py > plone.nix
