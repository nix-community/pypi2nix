import subprocess
from urllib.parse import urldefrag, urlparse

import click

from .utils import cmd, prefetch_git


class UnsupportedUrlError(Exception):
    pass


class OverridesFile(object):
    def __init__(self, path):
        self.path = path

    expression_template = 'import %(path)s { inherit pkgs python ; }'

    def nix_expression(self):
        return self.expression_template % dict(path=self.path)


class OverridesUrl(object):
    def __init__(self, url):
        self.url = url

    expression_template = (
        'let src = pkgs.fetchurl { ' +
        'url = %(url)s; sha256 = "%(sha_string)s"; ' +
        '}; in ' +
        'import "${src}" { inherit pkgs python ; }'
    )

    def nix_expression(self):
        command = 'nix-prefetch-url {url}'.format(
            url=self.url
        )

        return_code, output = cmd(
            command, verbose=False, stderr=subprocess.DEVNULL
        )
        sha_sum = output.strip()
        if len(sha_sum) != 52 or return_code != 0:
            raise click.ClickException(
                'Could not determin hash for url %{url}s' % dict(
                    url=self.url
                )
            )
        return self.expression_template % dict(
            url=self.url,
            sha_string=sha_sum
        )


class OverridesGit(object):
    def __init__(self, repo_url, path, rev=None):
        self.repo_url = repo_url
        self.path = path
        self.rev = rev

    expression_template = (
        'let src = pkgs.fetchgit { ' +
        'url = "%(url)s"; ' +
        'sha256 = "%(sha256)s"; ' +
        'rev = "%(rev)s"; ' +
        '} ; in import "${src}/%(path)s" { inherit pkgs python; }'
    )

    def nix_expression(self):
        repo_data = prefetch_git(self.repo_url, self.rev)
        return self.expression_template % dict(
            url=repo_data['url'],
            sha256=repo_data['sha256'],
            rev=repo_data['rev'],
            path=self.path
        )


def url_to_overrides(url_string):
    url = urlparse(url_string)
    if url.scheme == '':
        return OverridesFile(url.path)
    elif url.scheme == 'file':
        return OverridesFile(url.path)
    elif url.scheme == 'http' or url.scheme == 'https':
        return OverridesUrl(url.geturl())
    elif url.scheme.startswith('git+'):
        if not url.fragment:
            raise UnsupportedUrlError(
                ('Cannot handle overrides with no path given, offeding url was'
                 ' {url}.')
                .format(
                    url=url_string
                )
            )
        fragments = dict(
            map(lambda x: x.split('='), url.fragment.split('&'))
        )
        return OverridesGit(
            repo_url=urldefrag(url.geturl()[4:])[0],
            path=fragments['path'],
            rev=fragments.get('rev', None),
        )
    else:
        raise UnsupportedUrlError('Cannot handle common overrides url %s' %
                                  url_string)


class OverridesUrlParam(click.ParamType):
    name = 'url'

    def convert(self, value, param, ctx):
        try:
            return url_to_overrides(value)
        except UnsupportedUrlError as e:
            self.fail(str(e), param, ctx)


OVERRIDES_URL = OverridesUrlParam()
