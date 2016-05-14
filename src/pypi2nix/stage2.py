"""Parse metadata from .dist-info directories in a wheelhouse."""

import click
import glob
import json
import os.path as p
import pip.download
import pip.index
import pip.req

from pypi2nix.utils import TO_IGNORE, curry, safe


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


def parse(metadata):
    """Parse relevant information out of a metadata.json file."""
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


def try_candidates(distinfo):
    """Find the actual metadata json file from several possible names."""
    for cand in ('metadata.json', 'pydist.json'):
        fn = p.join(distinfo, cand)
        if p.exists(fn):
            with open(fn) as f:
                metadata = json.load(f)
                if metadata['name'].lower() in TO_IGNORE:
                    return
                else:
                    return parse(metadata)
    raise click.ClickException('unable to find json in %s' % distinfo)


@curry
def extract_metadata_from_wheelhouse(wheel_dir):
    '''
    once we have all the metadata we can create wheels and install them, so
    that metadata.json is produced for each package which we process to
    extract dependencies for packages
    '''

    click.secho(
        'Stage2: Extracting metadata from {}'.format(wheel_dir), fg='green')

    res = []
    for distinfo in glob.glob(p.join(wheel_dir, '*.dist-info')):
        click.secho('|-> %s' % p.basename(distinfo), fg='blue')
        tmp = try_candidates(distinfo)
        if tmp:
            res.append(tmp)
    return res
