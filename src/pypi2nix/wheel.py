# flake8: noqa: E501

import hashlib
import json
import os
from typing import Dict, List, Optional

import click
import pkg_resources
import requests
from pypi2nix.licenses import all_classifiers
from pypi2nix.utils import TO_IGNORE, cmd, safe

EXTENSIONS = ['.tar.gz', '.tar.bz2', '.tar', '.zip', '.tgz']
INDEX_URL = "https://pypi.python.org/pypi"

class WheelMetadata(dict):
    def __init__(self, name, version, dependencies, homepage, license,
                 description):
        self['name'] = name
        self['version'] = version
        self['dependencies'] = dependencies
        self['homepage'] = homepage
        self['license'] = license
        self['description'] = description


def process_metadata(wheel: str) -> Optional[WheelMetadata]:
    """Find the actual metadata json file from several possible names.
    """
    for _file in ('metadata.json', 'pydist.json'):
        wheel_file = os.path.join(wheel, _file)
        if os.path.exists(wheel_file):
            with open(wheel_file) as f:
                metadata = json.load(f)
                if metadata['name'].lower() in TO_IGNORE:
                    return None
                else:
                    return WheelMetadata(
                        name=metadata['name'],
                        version=metadata['version'],
                        dependencies=extract_deps(metadata),
                        homepage=safe(find_homepage(metadata)),
                        license=find_license(metadata),
                        description=safe(metadata.get('summary', '')),
                    )
    raise click.ClickException(
        "Unable to find metadata.json/pydist.json in `%s` folder." % wheel)


def find_license(item):
    license = None

    classifiers = item.get('classifiers', [])

    # find first license classifier
    all_classifiers_keys = all_classifiers.keys()
    license_classifiers = [i for i in filter(
        lambda x: x in all_classifiers_keys,
        classifiers
    )]
    for license_classifier in license_classifiers:
        license_nix = all_classifiers[license_classifier]
        if license_nix is not None:
            license = license_nix
            break

    if license is None:
        license = item.get('license', '')

        if license in ['LGPL with exceptions or ZPL', 'ZPL 2.1']:
            license = "licenses.zpl21"
        elif license in ['MIT', 'MIT License',
                         'MIT or Apache License, Version 2.0',
                         'The MIT License'
        ]:
            license = "licenses.mit"
        elif license in ['BSD', 'BSD License', 'BSD-like',
                         'BSD or Apache License, Version 2.0'] or \
                license.startswith('BSD -'):
            license = "licenses.bsdOriginal"
        elif license in ['Apache 2.0', 'Apache License 2.0', 'Apache 2',
                         'Apache License, Version 2.0',
                         'Apache License Version 2.0']:
            license = "licenses.asl20"
        elif license in ['GNU Lesser General Public License (LGPL), Version 3',
                         'LGPL']:
            license = "licenses.lgpl3"
        elif license in [
                'MPL 2.0',
                'MPL 2.0 (Mozilla Public License)',
                'MPL-2.0',
        ]:
            license = "licenses.mpl20"
        elif license in ['Python Software Foundation License']:
            license = "licenses.psfl"

        else:
            if len(license_classifiers) > 0:
                license = license_classifiers[0]
            else:
                click.echo(
                    "WARNING: Couldn't recognize license `{}` for `{}`".format(
                        license, item.get('name')))

            license = '"{}"' .format(safe(license))

    return license


def extract_deps(metadata):
    """Get dependent packages from metadata.

    Note that this is currently very rough stuff. I consider only the
    first 'requires' dataset in 'run_requires'. Other requirement sets
    like 'test_requires' are completely ignored.
    """
    deps = []
    if 'run_requires' in metadata:
        for item in metadata['run_requires']:
            if 'requires' in item:
                for line in item['requires']:
                    components = line.split()

                    dep = components[0]
                    dep = dep.split("==")[0]
                    dep = dep.split(">=")[0]
                    dep = dep.split("<=")[0]
                    dep = dep.split("<")[0]
                    dep = dep.split(">")[0]

                    if dep.lower() in TO_IGNORE:
                        continue

                    if '[' in dep:
                        deps.append(dep.split('[')[0])
                    else:
                        deps.append(dep)

    return list(set(deps))


def find_homepage(item):
    homepage = ''
    if 'extensions' in item and \
            'python.details' in item['extensions'] and \
            'project_urls' in item['extensions']['python.details']:
        homepage = item['extensions']['python.details']['project_urls'].get(
            'Home', ''
        )

    return homepage


def download_file(url, filename, chunk_size=2048):
    r = requests.get(url, stream=True, timeout=None)
    r.raise_for_status()  # TODO: handle this nicer

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def find_release(
        wheel_cache_dir,
        wheel: WheelMetadata,
        wheel_data
) -> Dict[str, str]:

    wheel_release = None

    _release_version = wheel['version']
    _releases = wheel_data['releases'].get(wheel['version'], [])

    # sometimes version in release list is not exact match and we need to use
    # pkg_resources's parse_version function to detect which release list is
    # correct
    if not _releases:
        for _version, _releases_tmp in wheel_data['releases'].items():
            if pkg_resources.parse_version(wheel['version']) == \
               pkg_resources.parse_version(_version):
                _release_version = _version
                _releases = _releases_tmp
                break

    # sometimes for some unknown reason release data is under other version.
    # example: https://pypi.python.org/pypi/radiotherm/json
    if not _releases:
        _base_version = (
            pkg_resources  # type: ignore
            .parse_version(wheel['version'])
            .base_version
        )
        for _releases_tmp in wheel_data['releases'].values():
            for _release_tmp in _releases_tmp:
                for _ext in EXTENSIONS:
                    if _release_tmp['filename'].endswith(wheel['version'] + _ext):
                        _release_version = wheel['version']
                        _releases = [_release_tmp]
                        break
                    if _release_tmp['filename'].endswith(_base_version + _ext):
                        _release_version = _base_version
                        _releases = [_release_tmp]
                        break

    # a release can come in different formats. formats we care about are
    # listed in EXTENSIONS variable
    for _release in _releases:
        for _ext in EXTENSIONS:
            if _release['filename'].endswith(_ext):
                wheel_release = _release
                break
        if wheel_release:
            break

    if not wheel_release:
        raise click.ClickException(
            "Unable to find release for package {name} of version "
            "{version}".format(**wheel))

    release = dict()
    release['url'] = wheel_release['url']
    digests = wheel_release.get('digests')
    release['hash_type'] = 'sha256'
    if digests:
        release['hash_value'] = wheel_release['digests']['sha256']  # noqa
    else:
        # download file if it doens not already exists
        filename = os.path.join(
            wheel_cache_dir, wheel_release['filename'])
        if not os.path.exists(filename):
            download_file(wheel_release['url'], filename)

        # calculate sha256
        with open(filename, 'rb') as f:
            hash = hashlib.sha256(f.read())
        release['hash_value'] = hash.hexdigest()

    return release
