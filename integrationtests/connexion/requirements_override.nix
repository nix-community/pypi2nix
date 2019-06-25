{ pkgs, python }:

self: super: {
  "jsonschema" = python.overrideDerivation super."jsonschema" (old: {
    buildInputs = old.buildInputs ++ [self."vcversioner"];
  });

  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."setuptools-scm"];
  });
}
