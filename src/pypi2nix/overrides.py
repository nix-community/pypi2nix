import urllib
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import no_type_check
from urllib.parse import urldefrag
from urllib.parse import urlparse

import click

from pypi2nix.logger import Logger
from pypi2nix.logger import StreamLogger
from pypi2nix.network_file import DiskTextFile
from pypi2nix.network_file import GitTextFile
from pypi2nix.network_file import NetworkFile
from pypi2nix.network_file import UrlTextFile

from .utils import prefetch_github


class UnsupportedUrlError(Exception):
    pass


class Overrides(metaclass=ABCMeta):
    @abstractmethod
    def nix_expression(self, logger: Logger) -> str:
        pass


class OverridesNetworkFile(Overrides):
    def __init__(self, network_file: NetworkFile) -> None:
        self._network_file = network_file

    def nix_expression(self, logger: Logger) -> str:
        return f"import ({self._network_file.nix_expression()}) {{ inherit pkgs python ; }}"


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


class NetworkFileParameter(click.ParamType):
    name = "url"

    @no_type_check
    def convert(self, value, param, ctx):
        try:
            return self._url_to_network_file(value)
        except UnsupportedUrlError as e:
            self.fail(str(e), param, ctx)

    def _url_to_network_file(self, url_string: str) -> NetworkFile:
        url = urlparse(url_string)
        if url.scheme == "":
            return DiskTextFile(url.path)
        elif url.scheme == "file":
            return DiskTextFile(url.path)
        elif url.scheme == "http" or url.scheme == "https":
            return UrlTextFile(url.geturl(), StreamLogger.stdout_logger())
        elif url.scheme.startswith("git+"):
            return self._handle_git_override_url(url, url_string)
        else:
            raise UnsupportedUrlError(
                "Cannot handle common overrides url %s" % url_string
            )

    def _handle_git_override_url(
        self, url: urllib.parse.ParseResult, url_string: str
    ) -> GitTextFile:
        if not url.fragment:
            raise UnsupportedUrlError(
                (
                    "Cannot handle overrides with no path given, offending url was"
                    " {url}."
                ).format(url=url_string)
            )
        fragments: Dict[str, str] = dict()
        for fragment_item in url.fragment.split("&"):
            try:
                fragment_name, fragment_value = fragment_item.split()
            except ValueError:
                raise UnsupportedUrlError(
                    f"Encountered deformed URL fragment `{fragment_item}` "
                    f"in url `{url_string}`"
                )
            else:
                fragments[fragment_name] = fragment_value
        return GitTextFile(
            repository_url=urldefrag(url.geturl()[4:])[0],
            path=fragments["path"],
            revision_name=fragments.get("rev", "master"),
            logger=StreamLogger.stdout_logger(),
        )


FILE_URL = NetworkFileParameter()
