from distutils2.errors import IrrationalVersionError
from distutils2.metadata import Metadata
from distutils2.pypi.errors import ProjectNotFound
from distutils2.pypi.simple import Crawler
from distutils2.version import suggest_normalized_version

import os
import sys


def get_metadata(egg_rel):
    """ fetch_metadata

    egg_rel.fetch_metadata() should do this, but seems to be broken"""
    egg_rel.download()
    tmp_path = egg_rel.unpack()
    sub_dir = os.listdir(tmp_path)[0]
    return Metadata(os.path.join(tmp_path, sub_dir, "PKG-INFO"))

metadata_map = {
    "Home-page": "homepage",
    "License": "license",
    "Summary": "description",
}

def nix_metadata(egg_rel):
    egg_metadata = get_metadata(egg_rel)
    res = ""
    for key in ["Home-page", "Summary", "License"]:
        nix_key = metadata_map[key]
        nix_metadata = egg_metadata.get(key, None)
        if nix_metadata != None:
            res += '      {0} = "{1}";\n'.format(nix_key, nix_metadata)
    return res

def to_nixname(name):
    return name.replace('.', '_').replace('-', '_').lower()

def to_dict(text):
    result = {}
    current_tree = []
    for line in text.split('\n'):
        if not line:
            continue

        egg = line.strip().split();
        egg_name, egg_version, egg_extra = egg[0], '', ''
        if len(egg) >= 2:
            egg_version = egg[1]
        if len(egg) >= 3:
            egg_extra = egg[2]
        egg_nixname = to_nixname(egg_name)

        tree_level = int(round((len(line) - len(line.lstrip(' '))) / 4.0))

        current_tree = current_tree[:tree_level]
        current_tree.append(egg_nixname)

        if egg_nixname.startswith('['):  # this mean we're dealing with extras
            if len(current_tree) >= 2:
                result[current_tree[-2]]['extras'].append(egg_nixname[1:-1])
            continue

        if len(current_tree) >= 2:
            result[current_tree[-2]]['requirements'].append(egg_nixname)

        if egg_nixname not in result:
            result[egg_nixname] = {
                'name': egg_name,
                'version': egg_version,
                'extras': [],
                'requirements': []
                }

        #to_dict(..., spaces=spaces+4)

    return result

PRE_TMPL = """
{ pkgs, python, buildPythonPackage }:

let plone42Packages = python.modules // rec {
  inherit python;
  inherit (pkgs) fetchurl stdenv;

"""

TMPL = """
  %(nixname)s = buildPythonPackage rec {
    name = "%(name)s";

    src = fetchurl {
      url = "%(url)s";
      %(hashname)s = "%(hashval)s";
    };
%(install_command)s%(build_inputs)s%(propagated_build_inputs)s
    doCheck = false;

    meta = {
%(metadata)s
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };
"""

POST_TMPL = """
  eggtestinfo = buildPythonPackage rec {
    name = "eggtestinfo-0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/e/eggtestinfo/${name}.tar.gz";
      md5 = "6f0507aee05f00c640c0d64b5073f840";
    };

    # circular dependencies
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';

    doCheck = false;

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];

    };
  };

}; in plone42Packages
"""


# These cannot be installed without some requirements
hard_requirements = {
    'products_cmfactionicons': 'eggtestinfo',
    'products_cmfcalendar': 'eggtestinfo',
    'products_cmfdefault': 'eggtestinfo',
    'products_cmfuid': 'eggtestinfo',
    'products_dcworkflow': 'eggtestinfo',
    'products_cmftopic': 'eggtestinfo',
    'pastescript': 'paste pastedeploy',
}

# don't package stuff we can use from the system python packages
system_packages = [
    'distribute',
    'lxml',
    'setuptools',
    'zc_buildout',
]

# The permissions for the skel dirs is changed by nix, which prevents
# the instance from being installed, let's skip it
ignore_packages = ['plone_recipe_zope2instance',]

install_command = """
    # ignore dependencies
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
"""


plonedeps = open("plonedeps", "r").read()
def buildout2nix():
    #eggs = to_dict(sys.stdin.read())
    eggs = to_dict(plonedeps)
    pypi = Crawler()

    bad_eggs = []
    not_found = []
    version_error = []
    print PRE_TMPL

    for nixname in sorted(eggs.keys()):
        if nixname in system_packages: continue
        if nixname in ignore_packages: continue
        egg = eggs[nixname]
        version = suggest_normalized_version(egg['version'])
        name = egg['name']
        if egg['extras']:
            name += '-'.join(egg['extras'])
        name += '-' + egg['version']
        try:
            egg_release = pypi.get_release(egg['name'] + '==' + version)
        except ProjectNotFound:
            not_found.append(egg['name'])
        except IrrationalVersionError:
            version_error.append(egg['name'])
        egg_dist = egg_release.dists['sdist'].url
        url = egg_dist['url']
        url = url.replace("http://a.pypi", "http://pypi")
        metadata = nix_metadata(egg_release)
        url = url.replace(name, "${name}")
        build_inputs = ''
        if url.endswith(".zip"):
            build_inputs = "\n    buildInputs = [ pkgs.unzip ];\n"
        propagated_build_inputs = ''
        if nixname in hard_requirements.keys():
            propagated_build_inputs = (
                "\n    propagatedBuildInputs = [ {0} ];\n"
        ).format(hard_requirements[nixname])
        print TMPL % {'nixname': nixname,
                      'name': name,
                      'url': url,
                      'hashname': egg_dist['hashname'],
                      'hashval': egg_dist['hashval'],
                      'build_inputs': build_inputs,
                      'propagated_build_inputs': propagated_build_inputs,
                      'install_command': install_command,
                      'metadata': metadata,
        }
    print POST_TMPL
    # print "# Not Found: {0}\n# Version Error: {1}".format(
    #     not_found, version_error)


