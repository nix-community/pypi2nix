"""Parse metadata from .dist-info directories in a wheelhouse."""
# flake8: noqa: E501

import hashlib
import json
import os.path
import tempfile
from typing import Dict, List

import click
import pkg_resources
import requests
from pypi2nix.requirement import Requirement, process_requirement_line
from pypi2nix.utils import TO_IGNORE, cmd, safe
from pypi2nix.wheel import (INDEX_URL, WheelMetadata, find_release,
                            process_metadata)


def process_wheel(
        wheel: WheelMetadata,
        sources: Dict[str, Requirement],
        index,
        wheel_cache_dir
):
    """
    """
    name = wheel['name']
    if name in sources:
        source = sources[name]
        release = source.get_release()
    else:
        url = "{}/{}/json".format(index, name)
        r = requests.get(url, timeout=None)
        r.raise_for_status()  # TODO: handle this nicer
        wheel_data = r.json()

        if not wheel_data.get('releases'):
            raise click.ClickException(
                "Unable to find releases for packge {name}".format(
                    name=name
                )
            )

        release = find_release(wheel_cache_dir, wheel, wheel_data)
    wheel.update(release)
    return wheel


def main(verbose, wheels: List[str], requirements_files, wheel_cache_dir, index=INDEX_URL,
         extra_sources={}):
    """Extract packages metadata from wheels dist-info folders.
    """

    sources_urls = [i['url'] for i in extra_sources.values()]
    # get url's from requirements_files
    sources = {}
    for requirements_file in requirements_files:
        with open(requirements_file) as f:
            lines = f.readlines()
            for line in lines:
                for req in process_requirement_line(
                        line,
                        sources_urls,
                        verbose
                ):
                    sources[req.get_name()] = req
    outputs: List[str] = []
    metadata = []

    if verbose > 1:
        click.echo("-- sources ---------------------------------------------------------------")
        click.echo(json.dumps(sources, sort_keys=True, indent=4))
        click.echo("--------------------------------------------------------------------------")

    try:
        def extract_wheel_metadata(wheel_path, outputs):
            outputs += ['|-> from %s' % os.path.basename(wheel_path)]
            if verbose != 0:
                click.echo('|-> from %s' % os.path.basename(wheel_path))

            wheel_metadata = process_metadata(wheel_path)
            if not wheel_metadata:
                return

            if wheel_metadata['name'] in TO_IGNORE:
                if verbose != 0:
                    click.echo('    SKIPPING')
                return

            if verbose > 1:
                click.echo("-- wheel_metadata --------------------------------------------------------")
                click.echo(json.dumps(wheel_metadata, sort_keys=True, indent=4))
                click.echo("--------------------------------------------------------------------------")
            return wheel_metadata

        wheel_data = map(
            lambda w: extract_wheel_metadata(w, outputs),
            wheels
        )
        for wheel_metadata in wheel_data:
            if wheel_metadata is None:
                continue
            metadata.append(process_wheel(
                wheel_metadata,
                sources,
                index,
                wheel_cache_dir
            ))
    except Exception as e:
        if verbose == 0:
            click.echo('\n'.join(outputs))
        raise e

    return metadata
