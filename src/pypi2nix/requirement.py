import hashlib
import os
import tempfile
from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List

import click
import requests
from pypi2nix.utils import cmd, concat


class Requirement(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_release(self) -> Dict[str, str]:
        pass


class GitRequirement(Requirement):
    def __init__(self, name, url, verbose: bool) -> None:
        self.name = name
        self.url = url
        self.verbose = verbose

    def get_name(self):
        return self.name

    def get_release(self):
        release = {}
        release['name'] = self.get_name()
        release['url'] = self.url
        release['hash_type'] = 'sha256'
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
        return_code, output = cmd(command, self.verbose != 0)
        if return_code != 0:
            raise click.ClickException(
                "URL {url} for package {name} is not valid.".format(
                    url=release['url'],
                    name=self.get_name()
                )
            )
        for output_line in output.split('\n'):
            output_line = output_line.strip()
            if output_line.startswith('hash is '):
                release['hash_value'] = output_line[len('hash is '):].strip()
            elif output_line.startswith('git revision is '):
                release['rev'] = output_line[len('git revision is '):].strip()

        if release.get('hash_value', None) is None:
            raise click.ClickException('Could not determine the hash from ouput:\n{output}'.format(  # noqa: E501
                output=output
            ))
        if release.get('rev', None) is None:
            raise click.ClickException('Could not determine the revision from ouput:\n{output}'.format(  # noqa: E501
                output=output
            ))
        return release


class HgRequirement(Requirement):
    def __init__(self, name, url, verbose: bool) -> None:
        self.name = name
        self.url = url
        self.verbose = verbose

    def get_name(self):
        return self.name

    def get_release(self):
        release = {}
        release['name'] = self.get_name()
        release['url'] = self.url
        release['hash_type'] = 'sha256'
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
        return_code, output = cmd(command, self.verbose != 0)
        if return_code != 0:
            raise click.ClickException("URL {url} for package {name} is not valid.".format(  # noqa: E501
                url=release['url'],
                name=self.get_name()
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
            raise click.ClickException('Could not determine the hash from ouput:\n{output}'.format(  # noqa: E501
                output=output
            ))
        if release.get('rev', None) is None:
            raise click.ClickException('Could not determine the revision from ouput:\n{output}'.format(  # noqa: E501
                output=output
            ))
        return release


class UrlRequirement(Requirement):
    def __init__(self, name, url, chunk_size=2048) -> None:
        self.name = name
        self.url = url
        self.chunk_size = chunk_size

    def get_name(self):
        return self.name

    def get_release(self):
        release = {}
        release['name'] = self.get_name()
        release['url'] = self.url
        release['hash_type'] = 'sha256'
        release['fetch_type'] = 'fetchurl'

        r = requests.get(release['url'], stream=True, timeout=None)
        r.raise_for_status()  # TODO: handle this nicer

        with tempfile.TemporaryFile() as fd:
            for chunk in r.iter_content(self.chunk_size):
                fd.write(chunk)
                fd.seek(0)
                hash = hashlib.sha256(fd.read())

        release['hash_value'] = hash.hexdigest()
        return release


class PathRequirement(Requirement):
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def get_name(self):
        return self.name

    def get_release(self):
        release = {}
        release['name'] = self.get_name()
        release['url'] = self.url
        release['hash_type'] = 'sha256'
        release['fetch_type'] = 'path'
        return release


def normalize_line(line: str) -> str:
    line = line.strip()
    if line.startswith('-e '):
        line = line[3:]
    return line


def process_requirement_line(
        line: str,
        sources_urls: List[str],
        verbose: bool
) -> List[Requirement]:
    line = normalize_line(line)

    if os.path.isdir(line) and line not in sources_urls:
        raise click.ClickException(
            "Source for path `%s` does not exists." % line
        )

    mappings: Dict[str, Callable[[str, str], List[Requirement]]] = {
        'git+': lambda name, url: [GitRequirement(name, url, verbose)],
        'hg+': lambda name, url: [HgRequirement(name, url, verbose)],
        'http://': lambda name, url: [UrlRequirement(name, url)],
        'https://': lambda name, url: [UrlRequirement(name, url)],
        'file://':
        lambda name, url: [PathRequirement(name, url.replace('file://', ''))],
    }
    requirements = handle_line(mappings, line)
    if len(requirements) == 0:
        if line.startswith('-r '):
            return handle_include_line(line, sources_urls, verbose)
        try:
            url, egg = line.split('#')
            name = egg.split('egg=')[1]
            if os.path.isdir(url):
                return [PathRequirement(name, url)]
        except (IndexError, ValueError):
            pass
    return requirements


def handle_include_line(line, sources_urls, verbose):
    """At this point we assume that only files are included and now urls"""
    include_location = line[2:].strip()
    with open(include_location) as f:
        return concat(
            map(
                lambda line: process_requirement_line(
                    line, sources_urls, verbose
                ),
                f.readlines()
            )
        )


def handle_line(
        mappings: Dict[str, Callable[[str, str], List[Requirement]]],
        line: str
) -> List[Requirement]:
    for (prefix, mapping) in mappings.items():
        if line.startswith(prefix):
            url, egg = line.split('#')
            try:
                name = egg.split('egg=')[1]
            except IndexError:
                raise click.ClickException(
                    ("Requirement starting with {prefix} "
                     "should end with #egg=<name>. Line `{line}` does "
                     "not end with egg=<name>").format(
                         prefix=prefix,
                         line=line
                     )
                )
            return mapping(name, url)
    return []
