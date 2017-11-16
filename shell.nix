{ src ? { outPath = ./.; name = "pypi2nix"; }
, nixpkgs ? <nixpkgs>
, pythonVersion ? "36"
}:

let
  pkgs = import nixpkgs {};
  pythonPackages = builtins.getAttr "python${pythonVersion}Packages" pkgs;
in import ./default.nix {
  inherit src pythonPackages;
  inherit (pkgs) stdenv fetchurl zip makeWrapper nix
    nix-prefetch-git nix-prefetch-hg;
}
