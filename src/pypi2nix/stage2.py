"""Parse metadata from .dist-info directories in a wheelhouse."""

import click
import hashlib
import json
import os.path
import requests

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
    r = requests.get(url, stream=True)
    r.raise_for_status()  # TODO: handle this nicer

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def process_wheel(cache_dir, wheel, index=INDEX_URL):
    """
    """

    url = "{}/{}/json".format(index, wheel['name'])
    r = requests.get(url)
    r.raise_for_status()  # TODO: handle this nicer
    wheel_data = r.json()

    if not wheel_data.get('releases'):
        raise click.ClickException(
            "Unable to find releases for packge {name}".format(**wheel))

    if not wheel_data['releases'].get(wheel['version']):
        raise click.ClickException(
            "Unable to find releases for package {name} of version "
            "{version}".format(**wheel))

    release = None
    for possible_release in wheel_data['releases'][wheel['version']]:
        for extension in EXTENSIONS:
            if possible_release['url'].endswith(extension):
                release = dict()
                release['url'] = possible_release['url']
                digests = possible_release.get('digests')
                release['hash_type'] = 'sha256'
                if digests:
                    release['hash_value'] = possible_release['digests']['sha256']  # noqa
                else:
                    # download file if it doens not already exists
                    filename = os.path.join(
                        cache_dir, possible_release['filename'])
                    if not os.path.exists(filename):
                        download_file(possible_release['url'], filename)

                    # calculate sha256
                    with open(filename, 'rb') as f:
                        hash = hashlib.sha256(f.read())
                    release['hash_value'] = hash.hexdigest()

            if release:
                break
        if release:
            break

    if not release:
        raise click.ClickException(
            "Unable to find source releases for package {name} of version "
            "{version}".format(**wheel))

    if release:
        wheel.update(release)

    return wheel


def main(wheels, cache_dir, index=INDEX_URL):
    """Extract packages metadata from wheels dist-info folders.
    """

    metadata = []
    for wheel in wheels:

        click.echo('|-> from %s' % os.path.basename(wheel))

        wheel_metadata = process_metadata(wheel)
        if not wheel_metadata:
            continue

        metadata.append(process_wheel(cache_dir, wheel_metadata, index))

    return metadata
