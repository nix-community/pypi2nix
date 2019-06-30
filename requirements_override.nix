{ pkgs, python }:

self: super: {

  "fancycompleter" = python.overrideDerivation super."fancycompleter" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "flake8-debugger" = python.overrideDerivation super."flake8-debugger" (old: {
    buildInputs = old.buildInputs ++ [ self."pytest-runner" ];
  });

  "importlib-metadata" = python.overrideDerivation super."importlib-metadata" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });
  "mccabe" = python.overrideDerivation super."mccabe" (old: {
    buildInputs = old.buildInputs ++ [ self."pytest-runner" ];
  });

  "pdbpp" = python.overrideDerivation super."pdbpp" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "pluggy" = python.overrideDerivation super."pluggy" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "py" = python.overrideDerivation super."py" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "pytest" = python.overrideDerivation super."pytest" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "zipp" = python.overrideDerivation super."zipp" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

}
