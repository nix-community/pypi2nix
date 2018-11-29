{ pkgs ? import <nixpkgs> {}
}:

let
  nix-gitignore-src = pkgs.fetchFromGitHub {
    owner = "siers";
    repo = "nix-gitignore";
    rev = "221d4aea15b4b7cc957977867fd1075b279837b3";
    sha256 = "0xgxzjazb6qzn9y27b2srsp2h9pndjh3zjpbxpmhz0awdi7h8y9m";
  };
  nix-gitignore = pkgs.callPackage nix-gitignore-src {};
  python = import ./requirements.nix { inherit pkgs; };
  version = pkgs.lib.fileContents ./src/pypi2nix/VERSION;
  # we need to move it to src/pypi2nix/templates/
  readLines = file: with pkgs.lib;
    splitString "\n" (removeSuffix "\n" (builtins.readFile file));
  fromRequirementsFile = file: pythonPackages:
    map (name: builtins.getAttr name pythonPackages) (readLines file);
in python.mkDerivation {
  name = "pypi2nix-${version}";
  src = nix-gitignore.gitignoreSource [] ./.;
  buildInputs = [];
  propagatedBuildInputs = fromRequirementsFile ./requirements.txt python.packages;
  #doCheck = true;
  # checkPhase = ''
  #   flake8 ${src}/src
  # '';
  # patchPhase = ''
  #   sed -i -e "s|default='nix-shell',|default='${nix.out}/bin/nix-shell',|" $out/pkgs/pypi2nix/cli.py
  #   sed -i -e "s|nix-prefetch-git|${nix-prefetch-git}/bin/nix-prefetch-git|" $out/pkgs/pypi2nix/utils.py
  #   sed -i -e "s|nix-prefetch-hg|${nix-prefetch-hg}/bin/nix-prefetch-hg|" $out/pkgs/pypi2nix/stage2.py
  # '';

  # commonPhase = ''
  #   mkdir -p $out/bin

  #   echo "#!${pythonEnv.interpreter}/bin/python" >  $out/bin/pypi2nix
  #   echo "import pypi2nix.cli" >> $out/bin/pypi2nix
  #   echo "pypi2nix.cli.main()" >> $out/bin/pypi2nix

  #   chmod +x $out/bin/pypi2nix

  #   export PYTHONPATH=$out/pkgs:$PYTHONPATH
  # '';


  # installPhase = commonPhase + ''
  #   wrapProgram $out/bin/pypi2nix \
  #       --prefix PYTHONPATH : "$PYTHONPATH" \
  #       --prefix PATH : "${pythonEnv.interpreter}/bin:${nix-prefetch-hg}/bin"
  # '';

  # shellHook = ''
  #   export home=`pwd`
  #   export out=/tmp/`pwd | md5sum | cut -f 1 -d " "`-$name

  #   rm -rf $out
  #   mkdir -p $out

  #   cd $out
  #   runHook unpackPhase
  #   runHook commonPhase
  #   cd $home

  #   export PATH=$out/bin:$PATH
  #   export PYTHONPATH=`pwd`/src:$PYTHONPATH
  # '';
  meta = {
    homepage = https://github.com/garbas/pypi2nix;
    description = "A tool that generates nix expressions for your python packages, so you don't have to.";
    maintainers = with pkgs.lib.maintainers; [ garbas ];
  };
}
