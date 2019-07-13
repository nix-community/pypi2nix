{ pkgs, python }:

self: super: {

  "awscli" = python.overrideDerivation super."awscli" (old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [
      pkgs.groff
      pkgs.less
    ];
  });

}
