{ }:

let

  pkgs = import <nixpkgs> {};

  inherit (pkgs) lib stdenv fetchurl unzip;

  mkDerivation = { ... } @ attrs:
    stdenv.mkDerivation attrs // {
      buildInputs = [ unzip ] ++ attrs.buildInputs;
    };

  mkDerivation = {
      name
    , md5 ? null
    , pypiurl ? "https://pypi.python.org/packages/source"
    , extension ? "tar.gz"
    , ... } @ attrs:
    let
      nameOnly = (builtins.parseDrvName name).name;
      nameFirstLetter = builtins.substring 0 1 onlyName;
    in stdenv.mkDerivation rec {
      inherit name;
      src = fetchurl {
        inherit md5;
        url = "${pypiurl}/${nameFirstLetter}/${name}.${extension}";
      };
    } // attrs;

in mkDerivation
  name = "plumbum-1.4.2";
  md5 = "38b526af9012a5282ae91dfe372cefd3";
}
