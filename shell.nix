{ src ? { outPath = ./.; name = "pypi2nix"; }
, nixpkgs ? <nixpkgs>
, pythonVersion ? "35"
}:

let
  pkgs = import nixpkgs {};
  python = (builtins.getAttr "python${pythonVersion}Packages" pkgs).python;
in import ./default.nix {
  inherit src python;
  inherit (pkgs) stdenv fetchurl zip makeWrapper;
}
