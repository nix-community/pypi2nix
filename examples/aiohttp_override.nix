{ pkgs, python }:

self: super: {

   "async-timeout" = python.overrideDerivation super."async-timeout" (old: {
      buildInputs = old.buildInputs ++ [ self."pytest-runner" ];
   });

   "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
      buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
   });

}
