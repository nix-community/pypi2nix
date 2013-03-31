{ }:

let
    pkgs = import <nixpkgs> { };
    plone43rc1Packages = import ./43rc1.nix {
        pkgs = pkgs;
        python = pkgs.python27;
        pythonPackages = pkgs.python27Packages;
    };

in

with pkgs;

buildEnv {
  name = "plone-dev-env";
  paths = [
    python27
    python27Packages.ipdb
    python27Packages.ipython
    python27Packages.distribute
    python27Packages.recursivePthLoader
    python27Packages.virtualenv
    plone43rc1Packages.plone
    plone43rc1Packages.pillow
    plone43rc1Packages.mailinglogger
    plone43rc1Packages.plone_recipe_zope2instance
    plone43rc1Packages.zc_recipe_egg
  ] ++ lib.attrValues python27.modules;
}
