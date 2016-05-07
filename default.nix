{ stdenv, fetchurl, python, zip, makeWrapper
, src ? { outPath = ./.; name = "pypi2nix"; }
}:

let
  deps = import ./src/pypi2nix/deps.nix { inherit fetchurl; };
  version = builtins.readFile ./VERSION;
in stdenv.mkDerivation rec {
  name = "pypi2nix-${version}";
  srcs = with deps; [ src pip click setuptools zcbuildout zcrecipeegg ];
  buildInputs = [ python zip makeWrapper ];
  sourceRoot = ".";

  postUnpack = ''
    mkdir -p $out/pkgs

    mv pip-*/pip                        $out/pkgs/pip
    mv click-*/click                    $out/pkgs/click
    mv setuptools-*/setuptools          $out/pkgs/setuptools
    mv zc.buildout-*/src/zc             $out/pkgs/zc
    mv zc.recipe.egg-*/src/zc/recipe    $out/pkgs/zc/recipe

    if [ "$IN_NIX_SHELL" != "1" ]; then
      if [ -e git-export ]; then
        mv git-export/src/pypi2nix      $out/pkgs/pypi2nix
      else
        mv pypi2nix*/src/pypi2nix       $out/pkgs/pypi2nix
      fi
    fi
  '';

  commonPhase = ''
    mkdir -p $out/bin

    echo "#!${python}/bin/python"  >  $out/bin/pypi2nix
    echo "import pypi2nix.cli"          >> $out/bin/pypi2nix
    echo "pypi2nix.cli.main()"          >> $out/bin/pypi2nix

    chmod +x $out/bin/pypi2nix

    export PYTHONPATH=$out/pkgs:$PYTHONPATH
  '';

  installPhase = commonPhase + ''
    wrapProgram $out/bin/pypi2nix --prefix PYTHONPATH : "$PYTHONPATH"
  '';

  shellHook = ''
    export home=`pwd`
    export out=/tmp/`pwd | md5sum | cut -f 1 -d " "`-$name

    rm -rf $out
    mkdir -p $out

    cd $out
    runHook unpackPhase
    runHook commonPhase
    cd $home

    export PATH=$out/bin:$PATH
    export PYTHONPATH=`pwd`/src:$PYTHONPATH
  '';
}
