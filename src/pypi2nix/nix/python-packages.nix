{ stdenv, lib, python, fetchurl, ensureNewerSourcesHook, makeSetupHook
, makeWrapper, unzip, fetchgit, deps, buildEnv, writeText }:
let
  emptyDerivation = writeText "empty"
    "true";
  otherInputs = {
    inherit stdenv lib fetchurl ensureNewerSourcesHook unzip makeSetupHook
      makeWrapper python fetchgit deps buildEnv;
    flit = null;
  };
  nixpkgs_path = (import <nixpkgs> {}).path;
  base = self: {
    callPackage = lib.callPackageWith (otherInputs // self);
    setuptools = self.callPackage ./setuptools.nix {};
    wrapPython =
      self.callPackage
      "${nixpkgs_path}/pkgs/development/interpreters/python/wrap-python.nix"
      {};
    mkPythonDerivation =
      lib.makeOverridable(
        self.callPackage
        "${nixpkgs_path}/pkgs/development/interpreters/python/mk-python-derivation.nix"
        {}
      );
    buildPythonPackage = self.callPackage
      "${nixpkgs_path}/pkgs/development/interpreters/python/build-python-package.nix" {};
    buildPythonEnv = self.callPackage
      "${nixpkgs_path}/pkgs/development/interpreters/python/wrapper.nix"
      {};
    bootstrapped-pip = self.callPackage ./bootstrap-pip.nix {};
    bootstrapped-pip-no-wheel = self.callPackage ./bootstrap-pip.nix { include_wheel = false; };
    buildPythonPackageNoWheel = self.callPackage
      "${nixpkgs_path}/pkgs/development/interpreters/python/build-python-package.nix"
      { bootstrapped-pip = self.bootstrapped-pip-no-wheel; };
    buildPythonPackageNoPip = self.callPackage
      "${nixpkgs_path}/pkgs/development/interpreters/python/build-python-package.nix"
      { bootstrapped-pip = emptyDerivation; };
    appdirs = self.callPackage ./appdirs.nix {};
    buildout_requirements = self.callPackage ./buildout_requirements.nix {};
    packaging = self.callPackage ./packaging.nix {};
    pip = self.callPackage ./pip.nix {};
    pyparsing = self.callPackage ./pyparsing.nix {};
    six = self.callPackage ./six.nix {};
    wheel = self.callPackage ./wheel.nix {};
    zc_buildout = self.callPackage ./zc_buildout.nix {};
    zc_recipe_egg = self.callPackage ./zc_recipe_egg.nix {};
    withPackages = self.callPackage ./with-packages.nix
      { pythonPackages = self;
        buildEnv = self.buildPythonEnv;
      };
  };
in
lib.fix' base
