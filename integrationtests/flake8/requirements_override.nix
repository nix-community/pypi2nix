{ pkgs, python }:

self: super: {
  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."setuptools-scm"];
  });
}
