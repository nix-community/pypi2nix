{ pkgs, python }:

self: super: {
  "setuptools" = super."setuptools".overrideDerivation (old: {
    pipInstallFlags = ["--ignore-installed"];
  });
}
