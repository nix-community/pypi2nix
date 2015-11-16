"""Parse metadata from .dist-info directories in a wheelhouse."""

import click
import glob
import json
import os.path as p
import pip.download
import pip.index
import pip.req

SESSION = pip.download.PipSession()
URL = 'https://pypi.python.org/simple/'


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
                    if components[0] not in ['setuptools']:
                        deps.append(components[0])
    return list(set(deps))


def parse(metadata_json):
    """Parse relevant information out of a metadata.json file."""
    with open(metadata_json) as f:
        metadata = json.load(f)
    name = metadata['name']
    version = metadata['version']

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
    }


def try_candidates(distinfo):
    """Find the actual metadata json file from several possible names."""
    for cand in ('metadata.json', 'pydist.json'):
        fn = p.join(distinfo, cand)
        if p.exists(fn):
            return parse(fn)
    raise click.ClickException('unable to find json in %s' % distinfo)


def do(wheel_dir):
    res = []
    for distinfo in glob.glob(p.join(wheel_dir, '*.dist-info')):
        click.secho('|-> %s' % p.basename(distinfo), fg='blue')
        res.append(try_candidates(distinfo))
    return res
