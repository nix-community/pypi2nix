{ pkgs ? import <nixpkgs> { }, }:

let
  pythonPackages = import ./requirements.nix { inherit pkgs; };

  version = "dev";

  sourceFilter = with pkgs.lib;
    with builtins;
    path: type:
    let
      name = baseNameOf (toString path);
      ignoreDirectories = directories:
        !(any (directory: directory == name && type == "directory")
          directories);
      ignoreFileTypes = types:
        !(any (type: hasSuffix ("." + type) name && type == "regular") types);
    in ignoreDirectories [
      "parsemon2.egg-info"
      "__pycache__"
      "build"
      "dist"
      ".mypy_cache"
    ] && ignoreFileTypes [ "pyc" ];

  source = pkgs.lib.cleanSourceWith {
    src = ./.;
    filter = sourceFilter;
  };

  pypi2nixFunction = { mkDerivation, lib, nixfmt, attrs, black, click, flake8
    , flake8-unused-arguments, isort, jinja2, mypy, nix-prefetch-github
    , packaging, parsley, pdbpp, pytest, pytest-cov, setuptools, setuptools-scm
    , toml, twine, git, jsonschema, bumpv, }:
    mkDerivation {
      name = "pypi2nix-${version}";
      src = source;
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
        nixfmt
        bumpv
      ];
      buildInputs = [ ];
      nativeBuildInputs = [ git ];
      propagatedBuildInputs = [
        attrs
        click
        jinja2
        nix-prefetch-github
        packaging
        parsley
        setuptools
        toml
        jsonschema
      ];
      dontUseSetuptoolsShellHook = true;
      checkPhase = ''
        nixfmt --check default.nix
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
        homepage = "https://github.com/nix-community/pypi2nix";
        description =
          "A tool that generates nix expressions for your python packages, so you don't have to.";
        maintainers = with lib.maintainers; [ seppeljordan ];
      };
    };

  callPackage = pkgs.lib.callPackageWith ({
    mkDerivation = pythonPackages.mkDerivation;
    lib = pkgs.lib;
    nixfmt = pkgs.nixfmt;
    git = pkgs.git;
  } // pythonPackages.packages);

in callPackage pypi2nixFunction { }
