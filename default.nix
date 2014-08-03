{ }:

with import <nixpkgs> { };

let

  unveil = python27.tool {
    wheel = python27.wheels.unveil;
    doInstallCheck = true;
    installCheckPhase = "$out/bin/unveil --help";
  };

in stdenv.mkDerivation rec {

  version = builtins.readFile ./VERSION;
  name = "pypi2nix-${version}";

  buildInputs = [
    zip
    python27
    unveil
  ];

}
