import os.path
from typing import Dict
from typing import Optional
from typing import Union

from pypi2nix.logger import Logger
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import prefetch_hg
from pypi2nix.utils import prefetch_url

PackageSource = Union["GitSource", "HgSource", "PathSource", "UrlSource"]


class GitSource:
    def __init__(self, url: str, revision: Optional[str] = None):
        self.url = url
        self._prefetch_data: Optional[Dict[str, str]] = None
        self._revision = revision

    def nix_expression(self) -> str:
        return "\n".join(
            [
                "pkgs.fetchgit {",
                '        url = "%(url)s";',
                '        %(hash_type)s = "%(hash_value)s";',
                '        rev = "%(rev)s";',
                "      }",
            ]
        ) % dict(
            url=self.url,
            hash_type="sha256",
            hash_value=self.hash_value(),
            rev=self.revision(),
        )

    def hash_value(self) -> str:
        return self.prefetch_data()["sha256"]

    def revision(self) -> str:
        return self.prefetch_data()["rev"]

    def prefetch_data(self) -> Dict[str, str]:
        if self._prefetch_data is None:
            self._prefetch_data = prefetch_git(self.url, self._revision)
        return self._prefetch_data


class HgSource:
    def __init__(
        self, url: str, logger: Logger, revision: Optional[str] = None
    ) -> None:
        self.url = url
        self._revision = revision
        self._prefetch_data: Optional[Dict[str, str]] = None
        self.logger = logger

    def nix_expression(self) -> str:
        return "\n".join(
            [
                "pkgs.fetchhg {{",
                '        url = "{url}";',
                '        sha256 = "{hash_value}";',
                '        rev = "{revision}";',
                "      }}",
            ]
        ).format(url=self.url, hash_value=self.hash_value(), revision=self.revision())

    def hash_value(self) -> str:
        return self.prefetch_data()["sha256"]

    def revision(self) -> str:
        return self.prefetch_data()["revision"]

    def prefetch_data(self) -> Dict[str, str]:
        if self._prefetch_data is None:
            self._prefetch_data = prefetch_hg(self.url, self.logger, self._revision)
        return self._prefetch_data


class UrlSource:
    def __init__(
        self, url: str, logger: Logger, hash_value: Optional[str] = None
    ) -> None:
        self.url = url
        self._hash_value = hash_value
        self.chunk_size = 2048
        self.logger = logger

    def nix_expression(self) -> str:
        return "\n".join(
            [
                "pkgs.fetchurl {{",
                '        url = "{url}";',
                '        sha256 = "{hash_value}";',
                "}}",
            ]
        ).format(url=self.url, hash_value=self.hash_value())

    def hash_value(self) -> str:
        if self._hash_value is None:
            self._hash_value = self.calculate_hash_value()
        return self._hash_value

    def calculate_hash_value(self) -> str:
        return prefetch_url(self.url, self.logger)


class PathSource:
    def __init__(self, path: str) -> None:
        self.path = path

    @property
    def _normalized_path(self) -> str:
        if os.path.isabs(self.path):
            return self.path
        else:
            head, tail = os.path.split(self.path)
            if head:
                return self.path
            else:
                return os.path.join(self.path, ".")

    def nix_expression(self) -> str:
        return self._normalized_path
