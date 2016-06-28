"""Parse metadata from .dist-info directories in a wheelhouse."""

import click
import glob
import json
import os.path 
import pip.download
import pip.index
import pip.req

from pypi2nix.utils import TO_IGNORE, safe


SESSION = pip.download.PipSession()
URL = 'https://pypi.python.org/simple/'


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


def parse_metadata(metadata):
    """Parse relevant information out of a metadata.json file.
    """
    name = metadata['name']
    version = metadata['version']

    try:
        finder = pip.index.PackageFinder(
            index_urls=[URL], session=SESSION, find_links=[],
            format_control=pip.index.FormatControl(set([':all:']), set([])))
        req = pip.req.InstallRequirement.from_line('%s==%s' % (name, version))
        link = finder.find_requirement(req, False)
        assert link.hash_name == 'md5'
        return {
            'name': name,
            'version': version,
            'url': link.url_without_fragment,
            'md5': link.hash,
            'deps': extract_deps(metadata),
            'homepage': safe(find_homepage(metadata)),
            'license': safe(metadata.get('license', '')),
            'description': safe(metadata.get('summary', '')),
        }

    except:
        return {
            'name': name,
            'version': version,
            'deps': extract_deps(metadata),
        }


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
                    return parse_metadata(metadata)
    raise click.ClickException(
        "Unable to find metadata.json/pydist.json in `%s` folder." %  wheel)


def main(wheels):
    """Extract packages metadata from wheels dist-info folders.
    """

    wheels_metadata = []
    for wheel in wheels:
        click.echo('|-> from %s' % os.path.basename(wheel))
        wheel_metadata = metadata(wheel)
        if wheel_metadata:
            wheels_metadata.append(wheel_metadata)
    return wheels_metadata
