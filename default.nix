{ pypi2nix ? { outPath = ./.; name = "pypi2nix"; }
, nixpkgs ? builtins.fetchTarball "https://github.com/NixOS/nixpkgs-channels/archive/77f8f35d57618c1ba456d968524f2fb2c3448295.tar.gz"

, pythonVersion ? "27"
}:

let

  pkgs = import nixpkgs {};
  python = (builtins.getAttr "python${pythonVersion}Packages" pkgs).python;
  deps = import ./src/pypi2nix/deps.nix { inherit fetchurl; };

  inherit (pkgs) fetchurl;
  inherit (pkgs.stdenv) mkDerivation;

in mkDerivation rec {
  version = builtins.readFile ./VERSION;
  name = "pypi2nix-${version}";
  srcs = with deps; [ pypi2nix pip click setuptools zcbuildout zcrecipeegg ];
  buildInputs = with pkgs; [ zip makeWrapper ];
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
