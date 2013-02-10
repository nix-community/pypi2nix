from distutils2.metadata import Metadata
from python2nix.config import METADATA_MAP

import os
import sys


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
