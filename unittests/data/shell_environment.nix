{ dummy_argument ? "hello" }:

let
  pkgs =  import <nixpkgs> {};
in
  pkgs."${dummy_argument}"
