import json
import re
from functools import lru_cache
from http.client import HTTPException
from typing import Optional
from typing import Union
from urllib.request import urlopen

from attr import attrib
from attr import attrs
from packaging.version import LegacyVersion
from packaging.version import Version
from packaging.version import parse as parse_version

from pypi2nix.logger import Logger
from pypi2nix.pypi_package import PypiPackage
from pypi2nix.pypi_release import PypiRelease
from pypi2nix.pypi_release import ReleaseType


@attrs(frozen=True)
class Pypi:
    _logger: Logger = attrib()
    _index: str = attrib(default="https://pypi.org/pypi")

    @lru_cache(maxsize=None)
    def get_package(self, name: str) -> PypiPackage:
        def get_release_type(package_type: str) -> ReleaseType:
            if package_type == "sdist":
                return ReleaseType.SOURCE
            elif package_type == "bdist_wheel":
                return ReleaseType.WHEEL
            else:
                self._logger.warning(
                    f"Found unexpected `packagetype` entry for package `{name}`"
                )
                return ReleaseType.UNKNOWN

        url = f"{self._index}/{name}/json"
        try:
            with urlopen(url) as response_buffer:
                metadata = json.loads(response_buffer.read().decode("utf-8"))
        except HTTPException:
            raise PypiFailed(
                f"Failed to download metadata information from `{url}`, given package name `{name}`"
            )
        releases = {
            PypiRelease(
                url=data["url"],
                sha256_digest=data["digests"]["sha256"],
                version=version,
                type=get_release_type(data["packagetype"]),
            )
            for version, release_list in metadata["releases"].items()
            for data in release_list
        }

        return PypiPackage(name=metadata["info"]["name"], releases=releases)

    def get_source_release(self, name: str, version: str) -> Optional[PypiRelease]:
        def version_tag_from_release_url(url: str) -> Union[Version, LegacyVersion]:
            extension = "|".join(
                map(re.escape, [".tar.gz", ".tar.bz2", ".tar", ".zip", ".tgz"])
            )
            regular_expression = r".*{name}-(?P<version>.*)(?P<extension>{extension})$".format(
                name=re.escape(name), extension=extension
            )
            result = re.match(regular_expression, url)
            if result:
                return parse_version(result.group("version"))
            else:
                message = f"Could not guess version of package from url `{url}`"
                self._logger.error(message)
                raise PypiFailed(message)

        package = self.get_package(name)
        source_releases = filter(
            lambda release: release.type == ReleaseType.SOURCE, package.releases
        )
        releases_for_version = filter(
            lambda release: version_tag_from_release_url(release.url)
            == parse_version(version),
            source_releases,
        )
        for release in releases_for_version:
            return release
        else:
            return None


class PypiFailed(Exception):
    pass
