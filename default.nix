{ }:


let

  pkgs = import <nixpkgs> { };

  inherit (pkgs) fetchurl;
  inherit (pkgs.stdenv) mkDerivation;

  deps = import ./src/pypi2nix/deps.nix { inherit fetchurl; };

in mkDerivation rec {
  version = builtins.readFile ./VERSION;
  name = "pypi2nix-${version}";
  srcs = with deps; [ ./. pip click setuptools zcbuildout zcrecipeegg ];
  buildInputs = with pkgs; [ zip ];
  sourceRoot = "pypi2nix";
  postUnpack = ''
    if [ "$IN_NIX_SHELL" != "1" ]; then
      mv pip-${deps.pipVersion}/pip pypi2nix/src/pip
      mv click-${deps.clickVersion}/click pypi2nix/src/click
      mv setuptools-${deps.setuptoolsVersion}/setuptools pypi2nix/src/setuptools
      mv zc.buildout-${deps.zcbuildoutVersion}/src/zc pypi2nix/src/zc
      mv zc.recipe.egg-${deps.zcrecipeeggVersion}/src/zc/recipe pypi2nix/src/zc/recipe
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

    mv $TMP_PATH/pip-${deps.pipVersion}/pip $TMP_PATH/pkgs/pip
    mv $TMP_PATH/click-${deps.clickVersion}/click $TMP_PATH/pkgs/click
    mv $TMP_PATH/setuptools-${deps.setuptoolsVersion}/setuptools $TMP_PATH/pkgs/setuptools
    mv $TMP_PATH/zc.buildout-${deps.zcbuildoutVersion}/src/zc $TMP_PATH/pkgs/zc
    mv $TMP_PATH/zc.recipe.egg-${deps.zcrecipeeggVersion}/src/zc/recipe $TMP_PATH/pkgs/zc/recipe

    echo -e "#!${pkgs.python}/bin/python\nimport pypi2nix.cli\npypi2nix.cli.main()" > $TMP_PATH/bin/pypi2nix
    chmod +x $TMP_PATH/bin/*

    export PATH=$TMP_PATH/bin:$PATH
    export PYTHONPATH=`pwd`/src:$TMP_PATH/pkgs

  '';
}
