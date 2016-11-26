{ pypi2nix ? { outPath = ./.; name = "pypi2nix"; }
, supportedSystems ? [ "x86_64-linux" "x86_64-darwin" ]
}:

let

  pkgs = import <nixpkgs> {};

  pkgFor = system:
    if builtins.elem system supportedSystems
      then import ./default.nix {
        inherit (pkgs) stdenv fetchurl zip makeWrapper nix nix-prefetch-scripts;
        python = pkgs.python35;
        src = pypi2nix;
      }
      else abort "Unsupported system type: ${system}";

  forEach = f:
    builtins.listToAttrs (map (system:
      { name = system;
        value = pkgs.lib.hydraJob (f system);
      }) supportedSystems);

  version = builtins.readFile ./src/pypi2nix/VERSION;

  self = {

    build = forEach pkgFor;

    release = pkgs.releaseTools.aggregate {
      name = "pypi2nix-${version}";
      meta.description = "Aggregate job containing the release-critical jobs.";
      constituents = (map (x: builtins.attrValues x) (with self; [ build ]));
    };

  };

in self
