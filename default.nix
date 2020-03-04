{ pkgs ? import <nixpkgs> { }, include_nixfmt ? false }:

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
    in ignoreDirectories [ "__pycache__" "build" "dist" ".mypy_cache" ]
    && ignoreFileTypes [ "pyc" ];

  source = pkgs.lib.cleanSourceWith {
    src = ./.;
    filter = sourceFilter;
  };

  pypi2nixFunction = { mkDerivation, lib, nixfmt, attrs, black, click, flake8
    , flake8-unused-arguments, isort, jinja2, mypy, nix-prefetch-github
    , packaging, parsley, pdbpp, pytest, pytest-cov, setuptools, setuptools-scm
    , toml, twine, git, jsonschema, bumpv, hypothesis, pyyaml }:
    mkDerivation {
      name = "pypi2nix-${version}";
      src = source;
      checkInputs = [
        black
        bumpv
        flake8
        flake8-unused-arguments
        hypothesis
        isort
        mypy
        pdbpp
        pytest
        pytest-cov
        twine
      ] ++ (if include_nixfmt then [ nixfmt ] else [ ]);
      buildInputs = [ ];
      nativeBuildInputs = [ git ];
      propagatedBuildInputs = [
        attrs
        click
        jinja2
        jsonschema
        nix-prefetch-github
        packaging
        parsley
        pyyaml
        setuptools
        setuptools-scm
        toml
      ];
      dontUseSetuptoolsShellHook = true;
      checkPhase = ''
        ${if include_nixfmt then "nixfmt --check default.nix" else ""}
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
