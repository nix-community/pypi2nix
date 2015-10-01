{ }:

let
  pkgs = import <nixpkgs> { };
in
  import ./src/pypi2nix/bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper python;
  }
