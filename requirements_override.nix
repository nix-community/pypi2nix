{ pkgs, python }:

self: super: {

  "pytest" = python.overrideDerivation super."pytest" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "pluggy" = python.overrideDerivation super."pluggy" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

}
