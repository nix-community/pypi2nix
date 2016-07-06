"""Parse metadata from .dist-info directories in a wheelhouse."""

import aiohttp
import asyncio
import click
import glob
import hashlib
import json
import os.path 

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


def metadata(wheel):
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
        "Unable to find metadata.json/pydist.json in `%s` folder." %  wheel)


async def fetch_metadata(session, url):
    """Fetch page asynchronously.

    :param session: Session of client
    :param url: Requested url
    """
    async with session.get(url) as response:
        with aiohttp.Timeout(2):
            async with session.get(url) as response:
                assert response.status == 200
                return await response.json()


def fetch_all_metadata(cache_dir, packages, index=INDEX_URL):
    """Yield JSON information obtained from PyPI index given an iterable of
       package names.
    """
    loop = asyncio.get_event_loop()
    conn = aiohttp.TCPConnector(verify_ssl=False)
    with aiohttp.ClientSession(loop=loop, connector=conn) as session:
        for package in packages:
            url = "{}/{}/json".format(index, package['name'])
            yield combine_metadata(cache_dir, session, loop, package, loop.run_until_complete(fetch_metadata(session, url)))
    loop.close()


async def download_file(session, url, filename, chunk_size=1024):
    async with session.get(url) as resp:
        with open(filename, 'wb') as f:
            while True:
                chunk = await resp.content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)


def combine_metadata(cache_dir, session, loop, old, new):
    if not new.get('releases'):
        raise click.ClickException(
            "Unable to find releases for packge {name}".format(**old))

    if not new['releases'].get(old['version']):
        raise click.ClickException(
            "Unable to find releases for package {name} of version "
            "{version}".format(**old))

    release = None
    releases = new['releases'][old['version']]
    for possible_release in releases:
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
                        loop.run_until_complete(download_file(session, possible_release['url'], filename))

                    # calculate sha256
                    with open(filename, 'rb') as f:
                        release['hash_value'] = hashlib.sha256(f.read()).hexdigest()

            if release:
                break
        if release:
            break

    if not release:
        raise click.ClickException(
            "Unable to find source releases for package {name} of version "
            "{version}".format(**old))

    old.update(release)

    return old


def main(wheels, cache_dir):
    """Extract packages metadata from wheels dist-info folders.
    """

    wheels_metadata = []
    for wheel in wheels:
        click.echo('|-> from %s' % os.path.basename(wheel))
        wheel_metadata = metadata(wheel)
        if wheel_metadata:
            wheels_metadata.append(wheel_metadata)

    return list(fetch_all_metadata(cache_dir, wheels_metadata))
