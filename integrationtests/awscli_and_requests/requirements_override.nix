{ pkgs, python }:

self: super: {

  "awscli" = python.overrideDerivation super."awscli" (old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [
      pkgs.groff
      pkgs.less
    ];
  });

  "python-dateutil" = python.overrideDerivation super."python-dateutil" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

}
