import os.path
import tempfile
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import Optional
from urllib.request import urlopen

from pypi2nix.logger import Logger
from pypi2nix.memoize import memoize
from pypi2nix.utils import cmd
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import prefetch_url


class NetworkFile(metaclass=ABCMeta):
    @abstractmethod
    def nix_expression(self) -> str:
        pass

    @abstractmethod
    def fetch(self) -> str:
        pass


class UrlTextFile(NetworkFile):
    def __init__(
        self,
        url: str,
        logger: Logger,
        sha256: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        self.url = url
        self._sha256 = sha256
        self._logger = logger
        self._name = name

    def nix_expression(self) -> str:
        fetchurl_arguments = f'url = "{self.url}";'
        fetchurl_arguments += f'sha256 = "{self.sha256}";'
        if self._name:
            fetchurl_arguments += f'name = "{self._name}";'
        return f"pkgs.fetchurl {{ {fetchurl_arguments} }}"

    @property  # type: ignore
    @memoize
    def sha256(self) -> str:
        if self._sha256:
            return self._sha256
        else:
            return prefetch_url(self.url, self._logger, name=self._name)

    def fetch(self) -> str:
        with urlopen(self.url) as content:
            return content.read().decode("utf-8")  # type: ignore


class GitTextFile(NetworkFile):
    def __init__(
        self, repository_url: str, revision_name: str, path: str, logger: Logger
    ) -> None:
        self.repository_url = repository_url
        self._revision_name = revision_name
        self.path = path
        self._logger = logger

    def nix_expression(self) -> str:
        fetchgit_arguments = f'url = "{self.repository_url}";'
        fetchgit_arguments += f'sha256 = "{self.sha256}";'
        fetchgit_arguments += f'rev = "{self.revision}";'
        fetchgit_expression = f"pkgs.fetchgit {{ {fetchgit_arguments} }}"
        return f'"${{ {fetchgit_expression } }}/{self.path}"'

    @property
    def revision(self) -> str:
        return self._prefetch_data["rev"]  # type: ignore

    @property
    def sha256(self) -> str:
        return self._prefetch_data["sha256"]

    @property  # type: ignore
    @memoize
    def _prefetch_data(self) -> Dict[str, str]:
        return prefetch_git(self.repository_url, self._revision_name)

    @memoize
    def fetch(self) -> str:
        with tempfile.TemporaryDirectory() as target_directory:
            cmd(
                ["git", "clone", self.repository_url, target_directory],
                logger=self._logger,
            )
            cmd(
                ["git", "checkout", self._revision_name],
                logger=self._logger,
                cwd=target_directory,
            )
            with open(os.path.join(target_directory, self.path)) as f:
                return f.read()
