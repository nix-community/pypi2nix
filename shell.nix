{ src ? { outPath = ./.; name = "pypi2nix"; }
, nixpkgs ? builtins.fetchTarball "https://github.com/NixOS/nixpkgs-channels/archive/453086a15fc0db0c2bc17d98350b0632551cb0fe.tar.gz"

, pythonVersion ? "35"
}:

let
  pkgs = import nixpkgs {};
  python = (builtins.getAttr "python${pythonVersion}Packages" pkgs).python;
in import ./default.nix {
  inherit src python;
  inherit (pkgs) stdenv fetchurl zip makeWrapper;
}
