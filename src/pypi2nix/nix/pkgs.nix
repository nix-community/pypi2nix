{ pkgs ? import <nixpkgs> {}
, python ? (import <nixpkgs> {}).python
}:
let
  otherInputs = {
    inherit (pkgs) ensureNewerSourcesHook lib fetchurl unzip
      makeSetupHook fetchgit stdenv makeWrapper buildEnv writeText;
  };
  removePipSymlink = old: {
      postInstall = builtins.replaceStrings
        [''ln -s "$out/bin/pip3" "$out/bin/pip"''] [""] old.postInstall;
    };
  base = self: {
    # TODO: Remove this hack when nixpkgs python does not produce dead
    # symlinks anymore
    python = python.overrideDerivation( removePipSymlink );
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
    # we need to wrap python so that we can avoid leakage of python
    # environement into mercurial
    mercurial-wrapped = pkgs.stdenv.mkDerivation {
        name = "wrapped-mercurial";
        phases = [ "installPhase" ];
        buildInputs = [ pkgs.makeWrapper ];
        installPhase = ''
          mkdir $out/bin -p
          ln -s ${pkgs.mercurial}/bin/hg $out/bin/hg
          wrapProgram $out/bin/hg \
              --unset PYTHONPATH \
              --unset PYTHONHOME
        '';
      };
  };
in
pkgs.lib.fix' base
