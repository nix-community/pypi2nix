{ pkgs, python }:

self: super: {
  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    buildInputs = old.buildInputs ++ [self."setuptools-scm"];
  });
}
