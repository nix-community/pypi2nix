{ }:

with import <nixpkgs> { };

let

  python = python27;

  wheelsFor = python: self:
    let
      base = callPackage ../../../nixos/nixpkgs/pkgs/development/python-wheels/wheels-base.nix {} python self;
      meta =
        map (x: python.wheels.build x) (
          map (x: {
            name = x.name;
            src = fetchurl {
              url = x.url;
              ${x.hash_name} = x.hash;
            };
          })
          (lib.attrValues (
            builtins.fromJSON (builtins.readFile ./generated.json)
          ))
        );
      generated = import ./generated.nix python self;
    in
      base // (lib.mapAttrs
        (name: wheelspec:
          let
            wheel = self.build ((lib.attrByPath [name] {} meta) //
                                (lib.attrByPath [name] {} generated) //
                                wheelspec);
          in wheel)
        self);

  wheels = wheelsFor python wheels;

  wheelhouse = callPackage ../../../../nixos/nixpkgs/pkgs/development/python-wheels/wheelhouse.nix {};

  all = wheelhouse {
    name = "${python.libPrefix}-sentry-wheelhouse-all-wheels";
    wheels = lib.filter (x: x.isWheel or false) (lib.attrValues wheels);
  };

in 
 wheels // { inherit all; }
