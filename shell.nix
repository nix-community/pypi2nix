{ src ? { outPath = ./.; name = "pypi2nix"; }
, nixpkgs ? builtins.fetchTarball "https://github.com/NixOS/nixpkgs-channels/archive/77f8f35d57618c1ba456d968524f2fb2c3448295.tar.gz"

, pythonVersion ? "27"
}:

let
  pkgs = import nixpkgs {};
  python = (builtins.getAttr "python${pythonVersion}Packages" pkgs).python;
in import ./default.nix {
  inherit src python;
  inherit (pkgs) stdenv fetchurl zip makeWrapper;
}
