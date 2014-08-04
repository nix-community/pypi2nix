{ }:

with import <nixpkgs> { };

let

  wheelsFor = python: self:
    let
      base = pkgs.callPackage ../../nixpkgs/pkgs/development/python-wheels/wheels-base.nix {} python self;
      wheels =
        builtins.listToAttrs (
          map (x: {
            name = x.name;
            value = {
              name = x.spec_name;
              src = fetchurl {
                url = x.url;
                ${x.hash_name} = x.hash;
              };
            };
          })
          (lib.attrValues (
            builtins.fromJSON (builtins.readFile ./generated.json)
          ))
        );
     requires = {
       sentry.requires = lib.attrValues (
         lib.filterAttrs (n: w: (w.isWheel or false && n != "sentry")) self);
     };
   in
     base // (lib.mapAttrs (name: wheel:
      self.build ((lib.attrByPath [name] {} requires) // wheel)) wheels);

 wheels = wheelsFor python27 wheels;

in python27.tool {
  name = "sentry";
  wheel = lib.getAttr "sentry" wheels;
}
