import os

from pypi2nix.utils import PYTHON_VERSIONS, curry


def writer(f):
    return lambda x: f.write(x + '\n')


def find_license(license):
    if license == '"ZPL 2.1':
        license = "lib.zpt21"
    return license


def do_generate(metadata, generate_file):
    metadata_by_name = {x['name'].lower(): x for x in metadata}

    with open(generate_file, 'wa+') as f:
        write = writer(f)
        # TODO: write here the command that generated this file
        write("{ pkgs, python }:")
        write("")
        write("self: {")

        for item in metadata:
            write('  "%(name)s" = python.mkDerivation {' % item)
            write('    name = "%(name)s-%(version)s";' % item)
            if 'url' in item and 'md5' in item:
                write('    src = pkgs.fetchurl {')
                write('      url = "%(url)s";' % item)
                write('      md5 = "%(md5)s";' % item)
                write('    };')
            write('    doCheck = false;')
            write('    propagatedBuildInputs = [ %s ];' % ' '.join([
                'self."%(name)s"' % metadata_by_name[x.lower()]
                for x in item['deps'] if x.lower() in metadata_by_name]))
            write('    meta = {')
            write('      homepage = "%(homepage)s";' % item)
            write('      license = "%s";' % find_license(item['license']))
            write('      description = "%(description)s";' % item)
            write('    };')
            write('  };')

        write('}')


@curry
def generate_nix_expressions(metadata, input_name, input_file, python_version):
    '''With all above we can now generate nix expressions
    '''

    base_dir = os.getcwd()
    default_file = os.path.join(base_dir, '{}.nix'.format(input_name))
    generate_file = os.path.join(
        base_dir, '{}_generated.nix'.format(input_name))
    override_file = os.path.join(
        base_dir, '{}_override.nix'.format(input_name))

    with open(input_file) as f:
        do_generate(metadata, generate_file)

    if not os.path.exists(override_file):
        with open(override_file, 'wa+') as f:
            write = writer(f)
            write("{ pkgs, python }:")
            write("")
            write("self: super: {")
            write("}")

    # TODO: make sure we can configure the default.nix file name
    # TODO: for some reason default file gets overriden
    if not os.path.exists(default_file):
        with open(default_file, 'wa+') as f:
            write = writer(f)
            # TODO: include fromRequirements function
            write("{ system ? builtins.currentSystem")
            write(", nixpkgs ? <nixpkgs>")
            write("}:")
            write("")
            write("let")
            write("")
            write("  inherit (pkgs.stdenv.lib) fix' extends;")
            write("")
            write("  pkgs = import nixpkgs { inherit system; };")
            write("  pythonPackages = pkgs.%sPackages;" % (
                PYTHON_VERSIONS[python_version]))
            write("")
            write("  python = {")
            write("    interpreter = pythonPackages.python;")
            write("    mkDerivation = pythonPackages.buildPythonPackage;")
            write("    modules = pythonPackages.python.modules;")
            write("    overrideDerivation = drv: f: pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs);")  # noqa
            write("    pkgs = pythonPackages;")
            write("  };")
            write("")
            write("  generated = import %s { inherit pkgs python; };" % (
                generate_file))
            write("  overrides = import %s { inherit pkgs python; };" % (
                override_file))
            write("")
            write("in fix' (extends overrides generated)")
