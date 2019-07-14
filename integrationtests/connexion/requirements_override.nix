{ pkgs, python }:

self: super: {
  "jsonschema" = python.overrideDerivation super."jsonschema" (old: {
    buildInputs = old.buildInputs ++ [self."vcversioner"];
  });

  "pytest-runner" = super."pytest-runner".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."setuptools-scm"];
  });

  "mccabe" = super."mccabe".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."pytest-runner"];
  });

  "clickclick" = super."clickclick".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."flake8" self."six"];
  });

  "connexion" = super."connexion".overrideDerivation(old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [self."flake8"];
  });
}
