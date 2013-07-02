{ }:

let
    pkgs = import ../../nixpkgs { };
    plone43Packages = import ./4.3.1.nix {
        inherit pkgs;
        pythonPackages = pkgs.python27Packages;
    };
    sentryPackages = import ./../sentry/5.4.5.nix {
        inherit pkgs;
        pythonPackages = pkgs.python27Packages;
    };

in

with pkgs;

buildEnv {
  name = "plone-env";
  paths = [
    python27
#    python27Packages.ipdb
#    python27Packages.ipython
    python27Packages.distribute
    python27Packages.recursivePthLoader
    python27Packages.virtualenv
    plone43Packages.plone
    plone43Packages.pillow
    plone43Packages.mailinglogger
    plone43Packages.plone_recipe_zope2instance
    plone43Packages.plone_recipe_zeoserver
    plone43Packages.zc_recipe_egg
#    sentryPackages.raven
  ] ++ lib.attrValues python27.modules;
}
