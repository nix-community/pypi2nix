{ pkgs, python }:

self: super: {

  "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "BTrees" = python.overrideDerivation super."BTrees" (old: {
    propagatedBuildInputs =
      builtins.filter
        (x: (builtins.parseDrvName x.name).name != "${python.__old.python.libPrefix}-${python.__old.python.libPrefix}-ZODB")
        old.propagatedBuildInputs;
  });

}
