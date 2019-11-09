{
  pkgs ? import <nixpkgs> {},
}:

let
  pythonPackages = import ./requirements.nix { inherit pkgs; };

  version = pkgs.lib.fileContents ./src/pypi2nix/VERSION;

  pypi2nixFunction =
    { mkDerivation
    , lib

    , attrs
    , black
    , click
    , flake8
    , flake8-unused-arguments
    , isort
    , jinja2
    , mypy
    , nix-prefetch-github
    , parsley
    , pdbpp
    , pytest
    , pytest-cov
    , setuptools
    , toml
    , twine
    }: mkDerivation {
      name = "pypi2nix-${version}";
      src = ./.;
      checkInputs = [
        black
        flake8
        flake8-unused-arguments
        mypy
        isort
        pytest
        pytest-cov
        twine
        pdbpp
      ];
      buildInputs = [];
      propagatedBuildInputs = [
        attrs
        click
        jinja2
        nix-prefetch-github
        parsley
        setuptools
        toml
      ];
      dontUseSetuptoolsShellHook = true;
      checkPhase = ''
        echo "Running black ..."
        black --check --diff -v setup.py src/ unittests/ mypy/ integrationtests/ scripts/
        echo "Running flake8 ..."
        flake8 -v setup.py src/ integrationtests/ unittests/ scripts/
        mypy --config-file setup.cfg src/
        mypy \
            --config-file setup.cfg \
            unittests/ \
            conftest.py \
            integrationtests/ \
            --allow-untyped-defs \
            --ignore-missing-imports
        echo "Running pytest ..."
        PYTHONPATH=$PWD/src:$PYTHONPATH pytest -v unittests/ -m 'not nix'
      '';
      shellHook = ''
        export PATH=$PWD/scripts:$PATH
        export PYTHONPATH=$PWD/src:$PYTHONPATH
      '';
      meta = {
        homepage = https://github.com/nix-community/pypi2nix;
        description = "A tool that generates nix expressions for your python packages, so you don't have to.";
        maintainers = with lib.maintainers; [ seppeljordan ];
      };
    };

  callPackage = pkgs.lib.callPackageWith ({
    mkDerivation = pythonPackages.mkDerivation;
    lib = pkgs.lib;
  } // pythonPackages.packages);

in callPackage pypi2nixFunction {}
