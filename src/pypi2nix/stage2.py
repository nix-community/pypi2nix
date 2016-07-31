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
                        'license': safe(metadata.get('license', '')),
                        'description': safe(metadata.get('summary', '')),
                    }
    raise click.ClickException(
        "Unable to find metadata.json/pydist.json in `%s` folder." % wheel)


def download_file(url, filename, chunk_size=1024):
    r = requests.get(url, stream=True, timeout=3)
    r.raise_for_status()  # TODO: handle this nicer

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def find_release(cache_dir, wheel, wheel_data):

    wheel_release = None

    _releases = wheel_data['releases'].get(wheel['version'])
    if not _releases:
        _releases = wheel_data['releases'].values()
        _releases = list(itertools.chain.from_iterable(_releases))

    for _release in _releases:
        for _ext in EXTENSIONS:
            _filename = '{}-{}.{}'.format(
                wheel['name'], wheel['version'], _ext)
            if _release['filename'] == _filename:
                wheel_release = _release
                break
        if wheel_release:
            break

    if not wheel_release:
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
            cache_dir, wheel_release['filename'])
        if not os.path.exists(filename):
            download_file(wheel_release['url'], filename)

        # calculate sha256
        with open(filename, 'rb') as f:
            hash = hashlib.sha256(f.read())
        release['hash_value'] = hash.hexdigest()

    return release


def process_wheel(cache_dir, wheel, sources, index=INDEX_URL):
    """
    """

    if wheel['name'] in sources:
        release = dict()
        release['url'] = sources[wheel['name']]
        release['hash_type'] = 'sha256'

        r = requests.get(release['url'], stream=True, timeout=3)
        r.raise_for_status()  # TODO: handle this nicer

        chunk_size=1024
        with tempfile.TemporaryFile() as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
            fd.seek(0)
            hash = hashlib.sha256(fd.read())

        release['hash_value'] = hash.hexdigest()

    else:
        url = "{}/{}/json".format(index, wheel['name'])
        r = requests.get(url, timeout=3)
        r.raise_for_status()  # TODO: handle this nicer
        wheel_data = r.json()


        if not wheel_data.get('releases'):
            raise click.ClickException(
                "Unable to find releases for packge {name}".format(**wheel))

        release = find_release(cache_dir, wheel, wheel_data)

    wheel.update(release)

    return wheel


def main(wheels, requirements_files, cache_dir, index=INDEX_URL):
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

    metadata = []
    for wheel in wheels:

        click.echo('|-> from %s' % os.path.basename(wheel))

        wheel_metadata = process_metadata(wheel)
        if not wheel_metadata:
            continue

        metadata.append(
            process_wheel(cache_dir, wheel_metadata, sources, index))

    return metadata
