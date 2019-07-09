{ pkgs, python }:

self: super: {
  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    buildInputs = old.buildInputs ++ [self."setuptools-scm"];
  });

  "flake8" = super.flake8.overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [self."pep8"];
  });

  "mccabe" = super.mccabe.overrideDerivation(old: {
    buildInputs = old.buildInputs ++ [self."pytest-runner"];
  });
}
