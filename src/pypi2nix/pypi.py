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
from pypi2nix.pypi_release import get_release_type_by_packagetype


@attrs(frozen=True)
class Pypi:
    _logger: Logger = attrib()
    _index: str = attrib(default="https://pypi.org/pypi")

    @lru_cache(maxsize=None)
    def get_package(self, name: str) -> PypiPackage:
        def get_release_type(package_type: str) -> ReleaseType:
            release_type = get_release_type_by_packagetype(package_type)
            if release_type is None:
                self._logger.warning(
                    f"Found unexpected `packagetype` entry {package_type} for package `{name}`"
                )
                return ReleaseType.UNKNOWN
            else:
                return release_type

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
                filename=data["filename"],
            )
            for version, release_list in metadata["releases"].items()
            for data in release_list
        }

        return PypiPackage(
            name=metadata["info"]["name"],
            releases=releases,
            version=metadata["info"]["version"],
        )

    def get_source_release(self, name: str, version: str) -> Optional[PypiRelease]:
        def version_tag_from_filename(filename: str) -> Union[Version, LegacyVersion]:
            extension = "|".join(
                map(re.escape, [".tar.gz", ".tar.bz2", ".tar", ".zip", ".tgz"])
            )
            regular_expression = r"{name}-(?P<version>.*)(?P<extension>{extension})$".format(
                name=re.escape(name), extension=extension
            )
            result = re.match(regular_expression, filename)
            if result:
                return parse_version(result.group("version"))
            else:
                message = f"Could not guess version of package from url `{filename}`"
                self._logger.error(message)
                raise PypiFailed(message)

        package = self.get_package(name)
        source_releases = [
            release
            for release in package.releases
            if release.type == ReleaseType.SOURCE
        ]
        releases_for_version = (
            release
            for release in source_releases
            if parse_version(release.version) == parse_version(version)
        )

        for release in releases_for_version:
            return release
        else:
            releases_for_version_by_filename = (
                release
                for release in source_releases
                if version_tag_from_filename(release.filename) == parse_version(version)
            )
            for release in releases_for_version_by_filename:
                return release
            else:
                return None


class PypiFailed(Exception):
    pass
