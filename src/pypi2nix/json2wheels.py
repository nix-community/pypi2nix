import pypi2nix.cmd


def do(json_file='generated.json', wheels_file='generated.wheels'):

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
          ")'" % (json_file))

    # TODO: raise click exception
    if err:
        raise Exception(err)

    open(wheels_file, 'wb').write(out)

    return wheels_file
