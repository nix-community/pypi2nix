import subprocess
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import no_type_check
from urllib.parse import urldefrag
from urllib.parse import urlparse

import click

from pypi2nix.logger import Logger

from .utils import cmd
from .utils import prefetch_git
from .utils import prefetch_github


class UnsupportedUrlError(Exception):
    pass


class Overrides(metaclass=ABCMeta):
    @abstractmethod
    def nix_expression(self, logger: Logger) -> str:
        pass


class OverridesFile(Overrides):
    def __init__(self, path: str) -> None:
        self.path = path

    expression_template = "import %(path)s { inherit pkgs python ; }"

    def nix_expression(self, logger: Logger) -> str:  # noqa: U100
        return self.expression_template % dict(path=self.path)


class OverridesUrl(Overrides):
    def __init__(self, url: str) -> None:
        self.url = url

    expression_template = (
        "let src = pkgs.fetchurl { "
        + 'url = %(url)s; sha256 = "%(sha_string)s"; '
        + "}; in "
        + 'import "${src}" { inherit pkgs python ; }'
    )

    def nix_expression(self, logger: Logger) -> str:
        command = "nix-prefetch-url {url}".format(url=self.url)

        return_code, output = cmd(command, logger, stderr=subprocess.DEVNULL)
        sha_sum = output.strip()
        if len(sha_sum) != 52 or return_code != 0:
            raise click.ClickException(
                "Could not determine hash for url `{url}`".format(url=self.url)
            )
        return self.expression_template % dict(url=self.url, sha_string=sha_sum)


class OverridesGit(Overrides):
    def __init__(self, repo_url: str, path: str, rev: Optional[str] = None) -> None:
        self.repo_url = repo_url
        self.path = path
        self.rev = rev

    expression_template = (
        "let src = pkgs.fetchgit { "
        + 'url = "%(url)s"; '
        + 'sha256 = "%(sha256)s"; '
        + 'rev = "%(rev)s"; '
        + "fetchSubmodules = false; "
        + '} ; in import "${src}/%(path)s" { inherit pkgs python; }'
    )

    def nix_expression(self, logger: Logger) -> str:  # noqa: U100
        repo_data = prefetch_git(self.repo_url, self.rev)
        return self.expression_template % dict(
            url=repo_data["url"],
            sha256=repo_data["sha256"],
            rev=repo_data["rev"],
            path=self.path,
        )


class OverridesGithub(Overrides):
    def __init__(
        self, owner: str, repo: str, path: str, rev: Optional[str] = None
    ) -> None:
        self.owner = owner
        self.repo = repo
        self.path = path
        self.rev = rev

    def nix_expression(self, logger: Logger) -> str:  # noqa: U100
        prefetch_data = prefetch_github(self.owner, self.repo, self.rev)
        template = " ".join(
            [
                "let src = pkgs.fetchFromGitHub {{",
                'owner = "{owner}";',
                'repo = "{repo}";',
                'rev = "{rev}";',
                'sha256 = "{sha256}";',
                "}} ;",
                'in import "${{src}}/{path}" {{',
                "inherit pkgs python;",
                "}}",
            ]
        )
        return template.format(
            owner=self.owner,
            repo=self.repo,
            rev=prefetch_data["rev"],
            sha256=prefetch_data["sha256"],
            path=self.path,
        )


def url_to_overrides(url_string: str) -> Overrides:
    url = urlparse(url_string)
    if url.scheme == "":
        return OverridesFile(url.path)
    elif url.scheme == "file":
        return OverridesFile(url.path)
    elif url.scheme == "http" or url.scheme == "https":
        return OverridesUrl(url.geturl())
    elif url.scheme.startswith("git+"):
        if not url.fragment:
            raise UnsupportedUrlError(
                (
                    "Cannot handle overrides with no path given, offeding url was"
                    " {url}."
                ).format(url=url_string)
            )
        fragments: Dict[str, str] = dict()
        for fragment_item in url.fragment.split("&"):
            try:
                fragment_name, fragment_value = fragment_item.split()
            except ValueError:
                raise UnsupportedUrlError(
                    "Encountered deformed URL fragment `{}` in url `{}`".format(
                        fragment_item, url_string
                    )
                )
            else:
                fragments[fragment_name] = fragment_value
        return OverridesGit(
            repo_url=urldefrag(url.geturl()[4:])[0],
            path=fragments["path"],
            rev=fragments.get("rev", None),
        )
    else:
        raise UnsupportedUrlError("Cannot handle common overrides url %s" % url_string)


class OverridesUrlParam(click.ParamType):
    name = "url"

    @no_type_check
    def convert(self, value, param, ctx):
        try:
            return url_to_overrides(value)
        except UnsupportedUrlError as e:
            self.fail(str(e), param, ctx)


OVERRIDES_URL = OverridesUrlParam()
