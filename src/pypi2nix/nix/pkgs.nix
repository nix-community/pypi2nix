{ pkgs ? import <nixpkgs> {}
, python ? (import <nixpkgs> {}).python
}:
let
  otherInputs = {
    inherit (pkgs) ensureNewerSourcesHook lib fetchurl unzip
      makeSetupHook fetchgit stdenv makeWrapper buildEnv writeText;
  };
  base = self: {
    python = python;
    deps = self.callPackage ../deps.nix {};
    callPackage = pkgs.lib.callPackageWith (otherInputs // self);
    pythonPackages = self.callPackage ./python-packages.nix {};
    pypiEnv = self.pythonPackages.withPackages
      (p : with p; [
        buildout_requirements
        packaging
        pip
        six
        wheel
        zc_buildout
        zc_recipe_egg
      ]);
  };
in
pkgs.lib.fix' base
