args@{
  pkgs ? import <nixpkgs> {},
  ...
}:

let
  default = import ./default.nix (args // { doCheck = true; });
in
default
