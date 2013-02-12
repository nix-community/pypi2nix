from distutils2.metadata import Metadata
from distutils2.pypi.simple import Crawler
from distutils2.version import suggest_normalized_version
from python2nix.config import HARD_REQUIREMENTS
from python2nix.config import INSTALL_COMMAND
from python2nix.config import METADATA_MAP

import os


def get_metadata(egg_rel):
    """ fetch_metadata

    egg_rel.fetch_metadata() should do this, but seems to be broken"""
    egg_rel.download()
    tmp_path = egg_rel.unpack()
    sub_dir = os.listdir(tmp_path)[0]
    return Metadata(os.path.join(tmp_path, sub_dir, "PKG-INFO"))

def nix_metadata(egg_rel):
    egg_metadata = get_metadata(egg_rel)
    res = ""
    for key in ["Home-page", "Summary", "License"]:
        nix_key = METADATA_MAP[key]
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

        egg = line.strip().split()
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

def to_nix_dict(egg, nixname):
    """Return a dict of the package attributes relevant to a nix
    expression
    """
    pypi = Crawler()

    name = egg['name']
    if egg['extras']:
        name += '-'.join(egg['extras'])
    name += '-' + egg['version']

    version = suggest_normalized_version(egg['version'])
    egg_release = pypi.get_release(egg['name'] + '==' + version)
    egg_dist = egg_release.dists['sdist'].url
    url = egg_dist['url']
    url = url.replace("http://a.pypi", "http://pypi")
    url = url.replace(name, "${name}")

    build_inputs = ''
    if url.endswith(".zip"):
        build_inputs = "\n    buildInputs = [ pkgs.unzip ];\n"

    propagated_build_inputs = ''
    if HARD_REQUIREMENTS.has_key(nixname):
        propagated_build_inputs = (
            "\n    propagatedBuildInputs = [ {0} ];\n"
        ).format(HARD_REQUIREMENTS[nixname])

    return {
        'nixname': nixname,
        'name': name,
        'url': url,
        'hashname': egg_dist['hashname'],
        'hashval': egg_dist['hashval'],
        'build_inputs': build_inputs,
        'propagated_build_inputs': propagated_build_inputs,
        'install_command': INSTALL_COMMAND,
        'metadata': nix_metadata(egg_release),
    }
