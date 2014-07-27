{ }:

with import <nixpkgs> { };

let

in stdenv.mkDerivation rec {

  version = builtins.readFile ./VERSION;
  name = "pypi2nix-${version}";

  buildInputs = [
    zip
    python27
  ];

}
