{ }:

let
    pkgs = import <nixpkgs> { };
    sentryPackages = import ./5.4.5.nix {
        inherit pkgs;
        pythonPackages = pkgs.python27Packages;
    };

in

with pkgs;

buildEnv {
  name = "sentry-env";
  paths = [
    python27
    python27Packages.distribute
    python27Packages.recursivePthLoader
    python27Packages.virtualenv
    sentryPackages.sentry
  ] ++ lib.attrValues python27.modules;
}
