{ stdenv, fetchurl, zip, makeWrapper, nix, nix-prefetch-git, nix-prefetch-hg
, pythonPackages, nixpkgs
, src ? { outPath = ./.; name = "pypi2nix"; }
}:

let

  version = builtins.readFile ./src/pypi2nix/VERSION;

  pythonEnv = import ./requirements.nix { pkgs = nixpkgs; };

in stdenv.mkDerivation rec {
  name = "pypi2nix-${version}";
  inherit src;
  buildInputs = [
    pythonPackages.python pythonPackages.flake8
    zip makeWrapper nix.out nix-prefetch-git nix-prefetch-hg
  ];
  doCheck = true;
  sourceRoot = ".";

  postUnpack = ''
    mkdir -p $out/pkgs
    ls -la
    pwd
    if [ -e git-export/src/pypi2nix ]; then
      mv git-export/src/pypi2nix      $out/pkgs/pypi2nix;
    elif [ -e src/pypi2nix ]; then
      mv src/pypi2nix                 $out/pkgs/pypi2nix;
    elif [ -e pypi2nix*/src/pypi2nix ]; then
      mv pypi2nix*/src/pypi2nix       $out/pkgs/pypi2nix;
    else
      echo "!!! Could not find source for pypi2nix !!!";
      exit 123;
    fi
  '';

  patchPhase = ''
    sed -i -e "s|default='nix-shell',|default='${nix.out}/bin/nix-shell',|" $out/pkgs/pypi2nix/cli.py
    sed -i -e "s|nix-prefetch-git|${nix-prefetch-git}/bin/nix-prefetch-git|" $out/pkgs/pypi2nix/utils.py
    sed -i -e "s|nix-prefetch-hg|${nix-prefetch-hg}/bin/nix-prefetch-hg|" $out/pkgs/pypi2nix/stage2.py
  '';

  commonPhase = ''
    mkdir -p $out/bin

    echo "#!${pythonEnv.interpreter}/bin/python" >  $out/bin/pypi2nix
    echo "import pypi2nix.cli" >> $out/bin/pypi2nix
    echo "pypi2nix.cli.main()" >> $out/bin/pypi2nix

    chmod +x $out/bin/pypi2nix

    export PYTHONPATH=$out/pkgs:$PYTHONPATH
  '';

  checkPhase = ''
    flake8 ${src}/src
  '';

  installPhase = commonPhase + ''
    wrapProgram $out/bin/pypi2nix \
        --prefix PYTHONPATH : "$PYTHONPATH" \
        --prefix PATH : "${pythonEnv.interpreter}/bin:${nix-prefetch-hg}/bin"
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

  meta = {
    homepage = https://github.com/garbas/pypi2nix;
    description = "A tool that generates nix expressions for your python packages, so you don't have to.";
    maintainers = with stdenv.lib.maintainers; [ garbas ];
  };
}
