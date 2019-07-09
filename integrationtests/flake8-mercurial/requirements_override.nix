{ pkgs, python }:

self: super: {
  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    buildInputs = old.buildInputs ++ [self."setuptools-scm"];
  });

  "mccabe" = super.mccabe.overrideDerivation(old: {
    buildInputs = old.buildInputs ++ [self."pytest-runner"];
  });
}
