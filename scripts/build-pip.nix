with import <nixpkgs> {};
with python3Packages;

stdenv.mkDerivation {
  name = "impure-environment";
  buildInputs = [
    python3Packages.pip
    python3Packages.wheel
    python3Packages.setuptools
  ];
  shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
  '';
}
