import json

def do(json_file='generated.json', nix_file='generated.nix'):
    nix-build -E 'with import <nixpkgs> {}; map (x: python27.wheels.build x) ( map (x: { name = x.name; src = fetchurl { url = x.url; md5 = x.md5; }; }) (lib.attrValues (builtins.fromJSON (builtins.readFile ./generated.json))))' -I /home/rok/dev/nixos 1> tmp
