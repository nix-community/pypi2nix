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
  readLines = file: with pkgs.lib; splitString "\n" (removeSuffix "\n" (builtins.readFile file));
  removeAfter = delim: line:
    let split = pkgs.lib.splitString delim line; in
    if builtins.length split > 1 then builtins.head split else line;
  applyTransform = lines: transform: builtins.map transform lines;
  transforms =
    [ (removeAfter "#") # remove after comment
    ];
  fromRequirementsFile = file: pythonPackages:
    builtins.map (name: builtins.getAttr name pythonPackages)
      (builtins.filter (x: x != "")
        (builtins.foldl' applyTransform (readLines file) transforms));
in python.mkDerivation {
  name = "pypi2nix-${version}";
  src = nix-gitignore.gitignoreSource [] ./.;
  buildInputs = fromRequirementsFile ./requirements-dev.txt python.packages;
  propagatedBuildInputs = fromRequirementsFile ./requirements.txt python.packages;
  doCheck = true;
  checkPhase = ''
    black --check --diff -v setup.py src/
    flake8 -v setup.py src/
    # TODO: pytest
  '';
  meta = {
    homepage = https://github.com/garbas/pypi2nix;
    description = "A tool that generates nix expressions for your python packages, so you don't have to.";
    maintainers = with pkgs.lib.maintainers; [ garbas ];
  };
}
