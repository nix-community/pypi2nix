"""Parse metadata from .dist-info directories in a wheelhouse."""

import click
import hashlib
import json
import os.path
import requests
import tempfile
import itertools

from pypi2nix.utils import TO_IGNORE, safe


EXTENSIONS = ['tar.gz', 'tar.bz2', 'tar', 'zip', 'tgz']
INDEX_URL = "https://pypi.io/pypi"
INDEX_URL = "https://pypi.python.org/pypi"


def find_homepage(item):
    homepage = ''
    if 'extensions' in item and \
            'python.details' in item['extensions'] and \
            'project_urls' in item['extensions']['python.details']:
        homepage = item['extensions']['python.details'].get('Home', '')
    return homepage


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


all_classifiers = {
    'License :: Aladdin Free Public License (AFPL)': None,
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication': None,
    'License :: DFSG approved': None,
    'License :: Eiffel Forum License (EFL)': None,
    'License :: Free For Educational Use': None,
    'License :: Free For Home Use': None,
    'License :: Free for non-commercial use': None,
    'License :: Freely Distributable': None,
    'License :: Free To Use But Restricted': None,
    'License :: Freeware': None,
    'License :: Netscape Public License (NPL)': None,
    'License :: Nokia Open Source License (NOKOS)': None,
    'License :: OSI Approved': None,
    'License :: OSI Approved :: Academic Free License (AFL)': 'licenses.afl21',
    'License :: OSI Approved :: Apache Software License': None,
    'License :: OSI Approved :: Apple Public Source License': None,
    'License :: OSI Approved :: Artistic License': 'licenses.artistic2',
    'License :: OSI Approved :: Attribution Assurance License': None,
    'License :: OSI Approved :: BSD License': 'licenses.bsdOriginal',
    'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)': None,
    'License :: OSI Approved :: Common Public License': 'licenses.cpl10',
    'License :: OSI Approved :: Eiffel Forum License': 'licenses.efl20',
    'License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)': None,
    'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)': None,
    'License :: OSI Approved :: GNU Affero General Public License v3': 'licenses.agpl3',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)': 'licenses.agpl3Plus',
    'License :: OSI Approved :: GNU Free Documentation License (FDL)': 'licenses.fdl13',
    'License :: OSI Approved :: GNU General Public License (GPL)': 'licenses.gpl1',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)': 'licenses.gpl2',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)': 'licenses.gpl2Plus',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)': 'licenses.gpl3',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)': 'licenses.gpl3Plus',
    'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': 'licenses.lgpk2',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)': 'licenses.lgpl2Plus',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)': 'licenses.lgpl3',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)': 'licenses.lgpl3Plus',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)': 'licenses.lgpl2',
    'License :: OSI Approved :: IBM Public License': 'licenses.ipl10',
    'License :: OSI Approved :: Intel Open Source License': None,
    'License :: OSI Approved :: ISC License (ISCL)': 'licenses.isc',
    'License :: OSI Approved :: Jabber Open Source License': None,
    'License :: OSI Approved :: MIT License': 'licenses.mit',
    'License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)': None,
    'License :: OSI Approved :: Motosoto License': None,
    'License :: OSI Approved :: Mozilla Public License 1.0 (MPL)': 'licenses.mpl10',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)': 'licenses.mpl11',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)': 'licenses.mpl20',
    'License :: OSI Approved :: Nethack General Public License': None,
    'License :: OSI Approved :: Nokia Open Source License': None,
    'License :: OSI Approved :: Open Group Test Suite License': None,
    'License :: OSI Approved :: Python License (CNRI Python License)': None,
    'License :: OSI Approved :: Python Software Foundation License': 'licenses.psfl',
    'License :: OSI Approved :: Qt Public License (QPL)': None,
    'License :: OSI Approved :: Ricoh Source Code Public License': None,
    'License :: OSI Approved :: Sleepycat License': 'licenses.sleepycat',
    'License :: OSI Approved :: Sun Industry Standards Source License (SISSL)': None,
    'License :: OSI Approved :: Sun Public License': None,
    'License :: OSI Approved :: University of Illinois/NCSA Open Source License': 'licenses.ncsa',
    'License :: OSI Approved :: Vovida Software License 1.0': 'licenses.vsl10',
    'License :: OSI Approved :: W3C License': 'licenses.w3c',
    'License :: OSI Approved :: X.Net License': None,
    'License :: OSI Approved :: zlib/libpng License': 'licenses.zlib',
    'License :: OSI Approved :: Zope Public License': 'licenses.zpt21',
    'License :: Other/Proprietary License': None,
    'License :: Public Domain': 'licenses.publicDomain',
    'License :: Repoze Public License': None,
}


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
            license = "licenses.zpt21"
        elif license in ['MIT', 'MIT License',
                         'MIT or Apache License, Version 2.0']:
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
        elif license in ['MPL 2.0', 'MPL 2.0 (Mozilla Public License)']:
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


def process_metadata(wheel):
    """Find the actual metadata json file from several possible names.
    """
    for _file in ('metadata.json', 'pydist.json'):
        wheel_file = os.path.join(wheel, _file)
        if os.path.exists(wheel_file):
            with open(wheel_file) as f:
                metadata = json.load(f)
                if metadata['name'].lower() in TO_IGNORE:
                    return
                else:
                    return {
                        'name': metadata['name'],
                        'version': metadata['version'],
                        'deps': extract_deps(metadata),
                        'homepage': safe(find_homepage(metadata)),
                        'license': find_license(metadata),
                        'description': safe(metadata.get('summary', '')),
                    }
    raise click.ClickException(
        "Unable to find metadata.json/pydist.json in `%s` folder." % wheel)


def download_file(url, filename, chunk_size=2048):
    r = requests.get(url, stream=True, timeout=None)
    r.raise_for_status()  # TODO: handle this nicer

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def find_release(wheel_cache_dir, wheel, wheel_data):

    wheel_release = None

    _releases = wheel_data['releases'].get(wheel['version'])
    if not _releases:
        _releases = wheel_data['releases'].values()
        _releases = list(itertools.chain.from_iterable(_releases))

    for _release in _releases:
        for _ext in EXTENSIONS:
            _version_plus_ext = '-{}.{}'.format(wheel['version'], _ext)
            if _release['filename'].endswith(_version_plus_ext):
                wheel_release = _release
                break
        if wheel_release:
            break

    if not wheel_release:
        import pdb
        pdb.set_trace()
        raise click.ClickException(
            "Unable to find releases for package {name} of version "
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


def process_wheel(wheel_cache_dir, wheel, sources, index=INDEX_URL,
                  chunk_size=2048):
    """
    """

    if wheel['name'] in sources:
        release = dict()
        release['url'] = sources[wheel['name']]
        release['hash_type'] = 'sha256'

        r = requests.get(release['url'], stream=True, timeout=None)
        r.raise_for_status()  # TODO: handle this nicer

        with tempfile.TemporaryFile() as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
            fd.seek(0)
            hash = hashlib.sha256(fd.read())

        release['hash_value'] = hash.hexdigest()

    else:
        url = "{}/{}/json".format(index, wheel['name'])
        r = requests.get(url, timeout=None)
        r.raise_for_status()  # TODO: handle this nicer
        wheel_data = r.json()


        if not wheel_data.get('releases'):
            raise click.ClickException(
                "Unable to find releases for packge {name}".format(**wheel))

        release = find_release(wheel_cache_dir, wheel, wheel_data)

    wheel.update(release)

    return wheel


def main(wheels, requirements_files, wheel_cache_dir, index=INDEX_URL):
    """Extract packages metadata from wheels dist-info folders.
    """

    # get url's from requirements_files
    sources = dict()
    for requirements_file in requirements_files:
        with open(requirements_file) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('http://') or line.startswith('https://'):
                    url, egg = line.split('#')
                    name = egg.split('egg=')[1]
                    sources[name] = url

    output = ''
    metadata = []

    try:
        for wheel in wheels:

            output += '|-> from %s' % os.path.basename(wheel)

            wheel_metadata = process_metadata(wheel)
            if not wheel_metadata:
                continue

            metadata.append(
                process_wheel(wheel_cache_dir, wheel_metadata, sources, index))
    except Exception as e:
        click.echo(output)
        raise e

    return metadata
