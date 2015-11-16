{ }:
let
  pkgs = import <nixpkgs> { };
  pythonPackages = pkgs.python27Packages;
  generated = import ./sentry_generated.nix { inherit pkgs self pythonPackages; };
  overrides = import ./sentry_overwrite.nix { inherit pkgs self generated pythonPackages; };
  self = generated // overrides;
in self
