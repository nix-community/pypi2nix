{ }:

let

  pkgs = import <nixpkgs>;

  inherit (pkgs) lib fetchurl;

  python = pkgs.python;


  # fetch from pypi

  fetchpypi = { name, ... } @ attrs:
    let
      _name = (builtins.parseDrvName name).name;
      firstLetter = builtins.substring 0 1 _name;
    in fetchurl ({
      urls = builtins.concatLists (map (ext: [
          "https://pypi.python.org/packages/source/${firstLetter}/${drvName}/${fullName}.${ext}"
          "https://pypi.python.org/packages/source/${firstLetter}/${drvName}/${lib.toLower fullName}.${ext}"
        ]) [ "zip" "tar.gz" "tgz" ]);
        ${hashType} = ${hash}
    } // attrs);


  # wheels for bootstrapping wheels, don't use for anything else

  _argparse = if (python.isPy26 or false) then (stdenv.mkDerivation {
    name = "${python.libPrefix}-bootstrap-wheel-argparse-1.2.1";
    src = fetchurl {
      url = https://pypi.python.org/packages/source/a/argparse/argparse-1.2.1.tar.gz;
      md5 = "2fbef8cb61e506c706957ab6e135840c";
    };
    passthru = { inherit python; };
    installPhase =
      ''
        mkdir -p $out/${python.sitePackages}
        cp argparse.py $out/${python.sitePackages}/
      '';
  }) else null;

  _setuptools = stdenv.mkDerivation {
    name = "${python.libPrefix}-bootstrapwheel-setuptools-5.4.1";
    src = fetchurl {
      url = https://pypi.python.org/packages/3.4/s/setuptools/setuptools-5.4.1-py2.py3-none-any.whl;
      md5 = "5b7b07029ad2285d1cbf809a8ceaea08";
    };
    passthru = { inherit python; };
    buildInputs = [ unzip ];
    unpackPhase = "true";
    installPhase =
      ''
        mkdir -p $out/${python.sitePackages}
        unzip -d $out/${python.sitePackages} $src
      '';
  };

  _wheel = stdenv.mkDerivation {
    name = "${python.libPrefix}-bootstrapwheel-wheel-0.24.0";
    src = fetchurl {
      url = https://pypi.python.org/packages/py2.py3/w/wheel/wheel-0.24.0-py2.py3-none-any.whl;
      md5 = "4c24453cda2177fd42c5d62d6434679a";
    };
    passthru = { inherit python; };
    buildInputs = [ unzip ];
    unpackPhase = "true";
    installPhase =
      ''
        mkdir -p $out/${python.sitePackages}
        unzip -d $out/${python.sitePackages} $src 
      '';
  };

  _mkDerivation = requires:
    let
    in
      if disable then null else wheel;

  mkDerivation = _mkDerivation { inherit


in mkDerivation rec {
  name = "plumbum";
  src = fetchpypi {
    inherit name
    md5 = "38b526af9012a5282ae91dfe372cefd3";
  };
}
