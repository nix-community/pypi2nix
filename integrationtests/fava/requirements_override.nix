{ pkgs, python }:

self: super: {
  "setuptools-scm-git-archive" =
    super."setuptools-scm-git-archive".overrideDerivation
    (old: { buildInputs = old.buildInputs ++ [ self."setuptools-scm" ]; });
}
