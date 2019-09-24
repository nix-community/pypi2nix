{ pkgs, python }:

self: super:
let
  addBuildInput = package: old: {
    buildInputs = old.buildInputs ++ [ package ];
  };
in {
  "fancycompleter" = python.overrideDerivation super."fancycompleter"
    (addBuildInput self."setuptools-scm");

  "flake8-debugger" = python.overrideDerivation super."flake8-debugger"
    (addBuildInput self."pytest-runner");

  "mccabe" = python.overrideDerivation super."mccabe"
    (addBuildInput self."pytest-runner");

  "pdbpp" = python.overrideDerivation super."pdbpp"
    (addBuildInput self."setuptools-scm");

  "py" = python.overrideDerivation super."py"
    (addBuildInput self."setuptools-scm");
}
