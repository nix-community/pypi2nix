{ stdenv, fetchurl, python, zip, makeWrapper, nix, nix-prefetch-scripts
, src ? { outPath = ./.; name = "pypi2nix"; }
}:

let

  click = fetchurl {
    url = "https://pypi.python.org/packages/7a/00/c14926d8232b36b08218067bcd5853caefb4737cda3f0a47437151344792/click-6.6.tar.gz";
    sha256 = "1sggipyz52crrybwbr9xvwxd4aqigvplf53k9w3ygxmzivd1jsnc";
  };

  requests = fetchurl {
    url = "https://pypi.python.org/packages/2e/ad/e627446492cc374c284e82381215dcd9a0a87c4f6e90e9789afefe6da0ad/requests-2.11.1.tar.gz";
    sha256 = "0cx1w7m4cpslxz9jljxv0l9892ygrrckkiwpp2hangr8b01rikss";
  };

  version = builtins.readFile ./src/pypi2nix/VERSION;

in stdenv.mkDerivation rec {
  name = "pypi2nix-${version}";
  srcs = [
    src
    click
    requests
  ];
  buildInputs = [ python zip makeWrapper nix.out nix-prefetch-scripts ];
  sourceRoot = ".";

  postUnpack = ''
    mkdir -p $out/pkgs

    mv click-*/click                    $out/pkgs/click
    mv requests-*/requests              $out/pkgs/

    if [ "$IN_NIX_SHELL" != "1" ]; then
      if [ -e git-export ]; then
        mv git-export/src/pypi2nix      $out/pkgs/pypi2nix
      else
        mv pypi2nix*/src/pypi2nix       $out/pkgs/pypi2nix
      fi
    fi
  '';

  patchPhase = ''
    sed -i -e "s|default='nix-shell',|default='${nix.out}/bin/nix-shell',|" $out/pkgs/pypi2nix/cli.py
    sed -i -e "s|nix-prefetch-git|${nix-prefetch-scripts}/bin/nix-prefetch-git|" $out/pkgs/pypi2nix/stage2.py
  '';

  commonPhase = ''
    mkdir -p $out/bin

    echo "#!${python.interpreter}" >  $out/bin/pypi2nix
    echo "import pypi2nix.cli" >> $out/bin/pypi2nix
    echo "pypi2nix.cli.main()" >> $out/bin/pypi2nix

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

  meta = {
    homepage = https://github.com/garbas/pypi2nix;
    description = "A tool that generates nix expressions for your python packages, so you don't have to.";
    maintainers = with stdenv.lib.maintainers; [ garbas ];
  };
}
