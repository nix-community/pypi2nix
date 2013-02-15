from distutils2.errors import IrrationalVersionError
from distutils2.pypi.errors import ProjectNotFound
from python2nix.config import IGNORE_PACKAGES
from python2nix.config import POST_TMPL
from python2nix.config import PRE_TMPL
from python2nix.config import SYSTEM_PACKAGES
from python2nix.config import TMPL
from python2nix.utils import to_dict
from python2nix.utils import to_nix_dict

import argparse
import subprocess
import sys


def python2nix():
    """Takes a list of packages and versions as input, and outputs a
    nix expression for them

    TODO: 

    * (re-)add support for tl.eggdeps to add package requirements as
    propagatedBuildInputs
    * add a --no-deps option instead of having it as the default
    """
    parser = argparse.ArgumentParser(
        description='Create a Nix package attribute set from a python buildout'
    )
    parser.add_argument(
        '-b',
        '--buildout-path',
        help='path to a buildout executable (not implemented)',
    )
    parser.add_argument(
        '-i',
        '--input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help=(
            'path to a file which contains one package name followed by a '
            'version number per line'
        )
    )    
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        type=argparse.FileType('wb', 0),
        default=sys.stdout,
        help='path to output nix file',
    )

    args = parser.parse_args()

    if args.buildout_path is not None:
        raise Exception("Not implemented")
    else:
        eggs = to_dict(args.input.read())
    nix_write = args.output.write

    nix_write(PRE_TMPL)

    not_found = []
    version_error = []
    for nixname in sorted(eggs.keys()):
        if nixname in SYSTEM_PACKAGES: continue
        if nixname in IGNORE_PACKAGES: continue
        egg = eggs[nixname]
        try:
            args.output.write(TMPL % to_nix_dict(egg, nixname))
        except ProjectNotFound:
            not_found.append(egg['name'])
        except IrrationalVersionError:
            version_error.append(egg['name'])

    nix_write(POST_TMPL)
    nix_write(
        "# Not Found: {0}\n# Version Error: {1}".format(
            not_found, version_error)
    )

def nix_list_python_packages():
    """Output a list of python packages already available in nixpkgs,
    one line per package and with the version following the name,
    separated by a space.

    Currently it just searches for packages whose name begins with
    "python-".
    """

    parser = argparse.ArgumentParser(
        description='List python packages already available in nixpkgs'
    )
    parser.add_argument(
        '-f',
        '--file',
        nargs='?',
        type=str,
        help=(
            'Specifies the Nix expression used to obtain derivations. The '
            'default is ~/.nix-defexpr, but the path to a local copy of '
            'nixpkgs can also be used e.g. '
            'my-git-repo/nixpkgs/pkgs/top-level/all-packages.nix'
        )
    )    
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        type=argparse.FileType('wb', 0),
        default=sys.stdout,
        help='path to the file to write the list of python packages to',
    )

    args = parser.parse_args()

    py_write = args.output.write

    command = 'nix-env -qa *'.split(" ")
    if args.file:
        command.append(['-f', args.file])

    def split_name_version(name):
        split_name = name.split("-")
        for i, segment in enumerate(split_name):
            if segment[0].isdigit():
                return '-'.join(split_name[:i]), '-'.join(split_name[i:])

    nix_pkgs = subprocess.check_output(command)
    for pkg in nix_pkgs.split('\n'):
        if pkg.startswith('python-'):
            name_version = split_name_version(pkg)
            if name_version:
                name, version = name_version
                if name != "python":
                    name = name[7:]
                    py_write('{0} {1}\n'.format(name, version))
