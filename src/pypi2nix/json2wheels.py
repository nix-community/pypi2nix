import pypi2nix.cmd


def do(json_file='generated.json', wheels_file='generated.wheels',
       nix_path=''):

    if nix_path != '':
        nix_path = '-I ' + nix_path

    out, err = pypi2nix.cmd.do(
        "nix-build -E '"
          "with import <nixpkgs> {}; "
          "map (x: python27.wheels.build x) ( "
            "map (x: { "
                "name = x.name; "
                "src = fetchurl { "
                    "url = x.url; "
                    "${x.hash_name} = x.hash; "
                "};"
            "})"
            "(lib.attrValues ("
                "builtins.fromJSON (builtins.readFile ./%s)"
            "))"
          ")' %s" % (json_file, nix_path))
    if err:
        raise Exception(err)

    open(wheels_file, 'wb').write(out)

    return wheels_file
