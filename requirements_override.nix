{ pkgs, python }:

self: super:
let
  addBuildInputs = packages: old: {
    buildInputs = old.buildInputs ++ packages;
  };
  pipInstallIgnoresInstalled = old: {
    pipInstallFlags = ["--ignore-installed"];
  };
  addSingleBuildInput = package: addBuildInputs [package];
  overridePythonPackage = name: overrides:
    let
      combinedOverrides = old: pkgs.lib.fold
        (override: previous: previous // override previous)
        old
        overrides;
    in python.overrideDerivation super."${name}" combinedOverrides;
in {
  "fancycompleter" = overridePythonPackage "fancycompleter"
    [
      (addBuildInputs [self."setuptools-scm"])
    ];

  "flake8-debugger" = overridePythonPackage "flake8-debugger"
    [
      (addBuildInputs [self."pytest-runner"])
    ];

  "mccabe" = overridePythonPackage "mccabe"
    [
      (addBuildInputs [self."pytest-runner"])
    ];

  "pdbpp" = overridePythonPackage "pdbpp"
    [
      (addBuildInputs [self."setuptools-scm"])
    ];

  "py" = overridePythonPackage "py"
    [
      (addBuildInputs [self."setuptools-scm"])
    ];

  "setuptools" = overridePythonPackage "setuptools"
    [
      pipInstallIgnoresInstalled
    ];
}
