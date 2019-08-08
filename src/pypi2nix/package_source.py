from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import click
import pkg_resources

from pypi2nix.logger import Logger
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import prefetch_hg
from pypi2nix.utils import prefetch_url
from pypi2nix.wheel import Wheel

EXTENSIONS = [".tar.gz", ".tar.bz2", ".tar", ".zip", ".tgz"]


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

    def nix_expression(self) -> str:
        return self.path


def find_release(wheel: Wheel, wheel_data: Dict[str, Any], logger: Logger) -> UrlSource:

    wheel_release = None

    _releases = wheel_data["releases"].get(wheel.version, [])

    # sometimes version in release list is not exact match and we need to use
    # pkg_resources's parse_version function to detect which release list is
    # correct
    if not _releases:
        for _version, _releases_tmp in wheel_data["releases"].items():
            if pkg_resources.parse_version(
                wheel.version
            ) == pkg_resources.parse_version(_version):
                _releases = _releases_tmp
                break

    # sometimes for some unknown reason release data is under other version.
    # example: https://pypi.python.org/pypi/radiotherm/json
    if not _releases:
        _base_version = pkg_resources.parse_version(  # type: ignore
            wheel.version
        ).base_version
        for _releases_tmp in wheel_data["releases"].values():
            for _release_tmp in _releases_tmp:
                for _ext in EXTENSIONS:
                    if _release_tmp["filename"].endswith(wheel.version + _ext):
                        _releases = [_release_tmp]
                        break
                    if _release_tmp["filename"].endswith(_base_version + _ext):
                        _releases = [_release_tmp]
                        break

    # a release can come in different formats. formats we care about are
    # listed in EXTENSIONS variable
    for _release in _releases:
        for _ext in EXTENSIONS:
            if _release["filename"].endswith(_ext):
                wheel_release = _release
                break
        if wheel_release:
            break

    if not wheel_release:
        raise click.ClickException(
            "Unable to find release for package {name} of version "
            "{version}".format(name=wheel.name, version=wheel.version)
        )

    sha256_digest: str = wheel_release.get("digests", {}).get("sha256", None)
    wheel_url: str = wheel_release["url"]
    return UrlSource(wheel_url, logger, sha256_digest)
