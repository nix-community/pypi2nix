{ pkgs, python }:

self: super: {

   "pyflakes" = python.overrideDerivation super."pyflakes" (old: {
      buildInputs = [ self."pytest-runner" ];
   });

   "mccabe" = python.overrideDerivation super."mccabe" (old: {
      buildInputs = [ self."pytest-runner" ];
   });

   "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
      buildInputs = [ self."setuptools-scm" ];
   });
}
