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
      ignoreEmacsFiles = !(hasPrefix ".#" name);
    in ignoreDirectories [
      "__pycache__"
      "build"
      "dist"
      ".mypy_cache"
      ".git"
      "integrationtests"
    ] && ignoreFileTypes [ "pyc" ] && ignoreEmacsFiles;

  source = pkgs.lib.cleanSourceWith {
    src = ./.;
    filter = sourceFilter;
  };

  pypi2nixFunction = { mkDerivation, lib, attrs, click, jinja2
    , nix-prefetch-github, packaging, parsley, setuptools, setuptools-scm, toml
    , jsonschema, hypothesis, pyyaml, }:
    mkDerivation {
      name = "pypi2nix-${version}";
      src = source;
      buildInputs = [ ];
      doCheck = false;
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
    git = pkgs.git;
    nix-prefetch-hg = pkgs.nix-prefetch-hg;
  } // pythonPackages.packages);

in callPackage pypi2nixFunction { }
