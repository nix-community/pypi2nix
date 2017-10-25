"""Parse metadata from .dist-info directories in a wheelhouse."""
# flake8: noqa: E501

import click
import hashlib
import json
import os.path
import requests
import tempfile
import pkg_resources

from pypi2nix.utils import TO_IGNORE, safe, cmd


EXTENSIONS = ['.tar.gz', '.tar.bz2', '.tar', '.zip', '.tgz']
INDEX_URL = "https://pypi.io/pypi"
INDEX_URL = "https://pypi.python.org/pypi"


def find_homepage(item):
    homepage = ''
    if 'extensions' in item and \
            'python.details' in item['extensions'] and \
            'project_urls' in item['extensions']['python.details']:
        homepage = item['extensions']['python.details']['project_urls'].get('Home', '')
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
    'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)': 'licenses.lgpl2',
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
    'License :: OSI Approved :: Zope Public License': 'licenses.zpl21',
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
        elif license in ['MPL 2.0', 'MPL 2.0 (Mozilla Public License)', 'MPL-2.0']:
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
        _base_version = pkg_resources.parse_version(wheel['version']).base_version
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


def process_wheel(wheel_cache_dir, wheel, sources, verbose, index=INDEX_URL,
                  chunk_size=2048):
    """
    """

    if wheel['name'] in sources:
        release = dict()
        release['url'] = sources[wheel['name']]['url']
        release['hash_type'] = 'sha256'

        repo_type = sources[wheel['name']]['type']
        if repo_type == 'url':

            release['fetch_type'] = 'fetchurl'

            r = requests.get(release['url'], stream=True, timeout=None)
            r.raise_for_status()  # TODO: handle this nicer

            with tempfile.TemporaryFile() as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)
                    fd.seek(0)
                    hash = hashlib.sha256(fd.read())

            release['hash_value'] = hash.hexdigest()

        elif repo_type == 'git':
            revision = ''
            if release['url'].startswith('git+'):
                release['url'] = release['url'][4:]
            if '@' in release['url']:
                release['url'], revision = release['url'].split('@')

            release['fetch_type'] = 'fetchgit'
            command = 'nix-prefetch-git {url} {revision}'.format(
                url=release['url'],
                revision=revision,
            )
            return_code, output = cmd(command, verbose != 0)
            if return_code != 0:
                raise click.ClickException("URL {url} for package {name} is not valid.".format(
                    url=release['url'],
                    name=wheel['name']
                ))
            for output_line in output.split('\n'):
                output_line = output_line.strip()
                if output_line.startswith('hash is '):
                    release['hash_value'] = output_line[len('hash is '):].strip()
                elif output_line.startswith('git revision is '):
                    release['rev'] = output_line[len('git revision is '):].strip()

            if release.get('hash_value', None) is None:
                raise click.ClickException('Could not determine the hash from ouput:\n{output}'.format(
                    output=output
                ))
            if release.get('rev', None) is None:
                raise click.ClickException('Could not determine the revision from ouput:\n{output}'.format(
                    output=output
                ))

        elif repo_type == 'hg':
            revision = ''
            if release['url'].startswith('hg+'):
                release['url'] = release['url'][3:]
            if '@' in release['url']:
                release['url'], revision = release['url'].split('@')

            release['fetch_type'] = 'fetchhg'
            command = 'nix-prefetch-hg {url} {revision}'.format(
                url=release['url'],
                revision=revision,
            )
            return_code, output = cmd(command, verbose != 0)
            if return_code != 0:
                raise click.ClickException("URL {url} for package {name} is not valid.".format(
                    url=release['url'],
                    name=wheel['name']
                ))
            HASH_PREFIX = 'hash is '
            REV_PREFIX = 'hg revision is '
            for output_line in output.split('\n'):
                print(output_line)
                output_line = output_line.strip()
                if output_line.startswith(HASH_PREFIX):
                    release['hash_value'] = output_line[len(HASH_PREFIX):].strip()
                elif output_line.startswith(REV_PREFIX):
                    release['rev'] = output_line[len(REV_PREFIX):].strip()

            if release.get('hash_value', None) is None:
                raise click.ClickException('Could not determine the hash from ouput:\n{output}'.format(
                    output=output
                ))
            if release.get('rev', None) is None:
                raise click.ClickException('Could not determine the revision from ouput:\n{output}'.format(
                    output=output
                ))

        elif repo_type == 'path':
            release['fetch_type'] = 'path'

        else:
            raise click.ClickException('Source type `{}` not implemented'.format(repo_type))

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


def main(verbose, wheels, requirements_files, wheel_cache_dir, index=INDEX_URL,
         sources=dict()):
    """Extract packages metadata from wheels dist-info folders.
    """

    # get url's from requirements_files
    sources_urls = [i['url'] for i in sources.values()]
    for requirements_file in requirements_files:
        with open(requirements_file) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('-e '):
                    line = line[3:]

                if os.path.isdir(line) and line not in sources_urls:
                    raise click.ClickException(
                        "Source for path `%s` does not exists." % line
                    )

                elif (line.startswith('http://') or
                      line.startswith('https://') or
                      line.startswith('git+') or
                      line.startswith('hg+')):
                    try:
                        url, egg = line.split('#')
                        name = egg.split('egg=')[1]
                        if line.startswith('git+'):
                            sources[name] = dict(url=url, type='git')
                        elif line.startswith('hg+'):
                            sources[name] = dict(url=url, type='hg')
                        else:
                            sources[name] = dict(url=url, type='url')
                    except:
                        raise click.ClickException(
                            "Requirement starting with http:// or https:// "
                            "should end with #egg=<name>. Line `-e %s` does "
                            "not end with egg=<name>" % line
                        )

    output = ''
    metadata = []

    if verbose > 1:
        click.echo("-- sources ---------------------------------------------------------------")
        click.echo(json.dumps(sources, sort_keys=True, indent=4))
        click.echo("--------------------------------------------------------------------------")

    try:
        for wheel in wheels:

            output += '|-> from %s' % os.path.basename(wheel)
            if verbose != 0:
                click.echo('|-> from %s' % os.path.basename(wheel))

            wheel_metadata = process_metadata(wheel)
            if not wheel_metadata:
                continue

            if wheel_metadata['name'] in TO_IGNORE:
                if verbose != 0:
                    click.echo('    SKIPPING')
                continue

            if verbose > 1:
                click.echo("-- wheel_metadata --------------------------------------------------------")
                click.echo(json.dumps(wheel_metadata, sort_keys=True, indent=4))
                click.echo("--------------------------------------------------------------------------")

            metadata.append(
                process_wheel(wheel_cache_dir, wheel_metadata, sources,
                              verbose, index))
    except Exception as e:
        if verbose == 0:
            click.echo(output)
        raise e

    return metadata
