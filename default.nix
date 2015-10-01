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

  clickName = "click-4.0";
  click = fetchurl {
    url = "https://pypi.python.org/packages/source/c/click/${clickName}.tar.gz";
    md5 = "79b475a1dbd566d8ce7daba5e6c1aaa7";
  };

  setuptoolsName = "setuptools-5.5.1";
  setuptools = fetchurl {
    url = "https://pypi.python.org/packages/source/s/setuptools/${setuptoolsName}.tar.gz";
    md5 = "86bbbfa732c234535316a7d74a49c6ad";
  };

  zcbuildoutName = "zc.buildout-2.4.3";
  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/source/z/zc.buildout/${zcbuildoutName}.tar.gz";
    md5 = "32dcb3de0673193b78d670c29551ef6c";
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
    if [ "$IN_NIX_SHELL" != "1" ]; then
      mv ${pipName}/pip pypi2nix/src/pip
      mv ${clickName}/click pypi2nix/src/click
      mv ${setuptoolsName}/setuptools pypi2nix/src/setuptools
      mv ${zcbuildoutName}/src/zc pypi2nix/src/zc
      mv ${zcrecipeeggName}/src/zc/recipe pypi2nix/src/zc/recipe
    fi
  '';

  installPhase = ''
    mkdir -p $out/bin
      cd src && zip -qr ../pypi2nix.zip * && cd ..
      echo '#!/usr/bin/env python' | cat - pypi2nix.zip > $out/bin/pypi2nix
      chmod +x $out/bin/pypi2nix
  '';

  # This package contains no binaries to patch or strip.
  dontPatchELF = true;
  dontStrip = true;

  shellHook = ''
    TMP_HOME=`pwd`
    TMP_PATH=/tmp/`pwd | md5sum | cut -f 1 -d " "`-$name

    rm -rf $TMP_PATH
    mkdir -p $TMP_PATH/bin $TMP_PATH/pkgs

    cd $TMP_PATH
    runHook unpackPhase
    cd $TMP_HOME

    mv $TMP_PATH/${pipName}/pip                    $TMP_PATH/pkgs/pip
    mv $TMP_PATH/${clickName}/click                $TMP_PATH/pkgs/click
    mv $TMP_PATH/${setuptoolsName}/setuptools      $TMP_PATH/pkgs/setuptools
    mv $TMP_PATH/${zcbuildoutName}/src/zc          $TMP_PATH/pkgs/zc
    mv $TMP_PATH/${zcrecipeeggName}/src/zc/recipe  $TMP_PATH/pkgs/zc/recipe

    echo "python -c 'import pypi2nix.cli; pypi2nix.cli.main()'" > $TMP_PATH/bin/pypi2nix
    chmod +x $TMP_PATH/bin/*

    export PATH=$TMP_PATH/bin:$PATH
    export PYTHONPATH=`pwd`/src:$TMP_PATH/pkgs

  '';
}
