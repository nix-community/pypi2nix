{ }:


let

  pkgs = import <nixpkgs> { };

  inherit (pkgs) fetchurl;
  inherit (pkgs.stdenv) mkDerivation;

  pipName = "pip-1.5.6";
  pip = fetchurl {
	  url = "https://pypi.python.org/packages/source/p/pip/${pipName}.tar.gz";
    md5 = "01026f87978932060cc86c1dc527903e";
  };

  clickName = "click-3.3";
  click = fetchurl {
		url = "https://pypi.python.org/packages/source/c/click/${clickName}.tar.gz";
    md5 = "40edaba4d216915a8326c5b2cb52781d";
  };

  setuptoolsName = "setuptools-5.5.1";
  setuptools = fetchurl {
		url = "https://pypi.python.org/packages/source/s/setuptools/${setuptoolsName}.tar.gz";
    md5 = "86bbbfa732c234535316a7d74a49c6ad";
  };

  zcbuildoutName = "zc.buildout-2.2.1";
  zcbuildout = fetchurl {
		url = "https://pypi.python.org/packages/source/z/zc.buildout/${zcbuildoutName}.tar.gz";
    md5 = "476a06eed08506925c700109119b6e41";
  };

  zcrecipeeggName = "zc.recipe.egg-2.0.1";
  zcrecipeegg = fetchurl {
		url = "https://pypi.python.org/packages/source/z/zc.recipe.egg/${zcrecipeeggName}.tar.gz";
    md5 = "5e81e9d4cc6200f5b1abcf7c653dd9e3";
  };

in mkDerivation rec {
  version = builtins.readFile ./VERSION;
  name = "pypi2nix-${version}";
  srcs = [ ./. pip click setuptools zcbuildout zcrecipeegg ];
  buildInputs = with pkgs; [ zip ];
  sourceRoot = "pypi2nix";
  postUnpack = ''
    mv ${pipName}/pip pypi2nix/src/pip
    mv ${clickName}/click pypi2nix/src/click
    mv ${setuptoolsName}/setuptools pypi2nix/src/setuptools
    mv ${zcbuildoutName}/src/zc pypi2nix/src/zc
    mv ${zcrecipeeggName}/src/zc/recipe pypi2nix/src/zc/recipe
  '';
  installPhase = ''
    mkdir $out/bin
	  cd src && zip -qr pypi2nix.zip * && cd ..
	  echo '#!/usr/bin/env python' | cat - $<pypi2nix.zip > $out/bin/pypi2nix
	  chmod +x $out/bin/pypi2nix
    ls -la $out/bin
  '';

}
