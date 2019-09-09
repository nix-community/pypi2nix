import email.parser
import os.path
from email.header import Header
from email.message import Message
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type

import click
import pkg_resources
from packaging.utils import canonicalize_name

from pypi2nix.license import find_license
from pypi2nix.logger import Logger
from pypi2nix.package_source import UrlSource
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import TO_IGNORE
from pypi2nix.utils import safe


class Wheel:
    def __init__(
        self,
        name: str,
        version: str,
        deps: RequirementSet,
        homepage: str,
        license: str,
        description: str,
        build_dependencies: RequirementSet,
    ):
        self.name = canonicalize_name(name)
        self.version = version
        self.deps = deps
        self.homepage = homepage
        self.license = license
        self.description = description
        self.build_dependencies: RequirementSet = build_dependencies

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "deps": [requirement.name() for requirement in self.deps],
            "homepage": self.homepage,
            "license": self.license,
            "description": self.description,
            "build_dependencies": [
                requirement.name() for requirement in self.build_dependencies
            ],
        }

    def add_build_dependencies(self, dependencies: RequirementSet) -> None:
        self.build_dependencies += dependencies

    @classmethod
    def _valid_dependency(constructor, name: str, dependency: str) -> bool:
        canonicalized_dependency = canonicalize_name(dependency)
        return all(
            [
                canonicalized_dependency != name,
                canonicalized_dependency not in TO_IGNORE,
            ]
        )

    @classmethod
    def from_wheel_directory_path(
        wheel_class: "Type[Wheel]",
        wheel_directory_path: str,
        target_platform: TargetPlatform,
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> "Wheel":
        metadata_file = os.path.join(wheel_directory_path, "METADATA")
        if os.path.exists(metadata_file):
            with open(
                metadata_file, "r", encoding="ascii", errors="surrogateescape"
            ) as headers:
                metadata = email.parser.Parser().parse(headers)
            license_string = str_from_message(metadata, "license")
            if license_string is None:
                license_string = ""
            classifiers = list_from_message(metadata, "classifiers")
            if classifiers is None:
                classifiers = []
            license = find_license(
                classifiers=classifiers, license_string=license_string
            )

            if license is None:
                license = '"' + safe(license_string) + '"'
                logger.warning(
                    "Couldn't recognize license `{}` for `{}`".format(
                        license_string, metadata.get("name")
                    )
                )

            name = str_from_message(metadata, "name")
            if name is None:
                raise Exception("Could not extract name from wheel metadata")
            else:
                name = canonicalize_name(name)

            version = str_from_message(metadata, "version")
            if version is None:
                raise Exception("Could not extract version from wheel metadata")

            dependencies = list_from_message(metadata, "requires-dist")
            if dependencies is None:
                dependencies = []

            description = str_from_message(metadata, "summary")
            if description is None:
                description = ""

            return wheel_class(
                name=name,
                version=version,
                deps=wheel_class._extract_deps(
                    dependencies,
                    target_platform,
                    requirement_parser,
                    current_wheel_name=name,
                ),
                homepage=safe(find_homepage(metadata)),
                license=license,
                description=safe(description),
                build_dependencies=RequirementSet(target_platform),
            )

        raise click.ClickException(
            "Unable to find METADATA in `%s` folder." % wheel_directory_path
        )

    @classmethod
    def _extract_deps(
        constructor,
        deps: Iterable[str],
        target_platform: TargetPlatform,
        requirement_parser: RequirementParser,
        current_wheel_name: str,
    ) -> RequirementSet:
        """Get dependent packages from metadata.

        Note that this is currently very rough stuff. I consider only the
        first 'requires' dataset in 'run_requires'. Other requirement sets
        like 'test_requires' are completely ignored.
        """
        extracted_deps = RequirementSet(target_platform)
        for dep_string in deps:
            dependency = requirement_parser.parse(dep_string)
            if dependency.name() in TO_IGNORE:
                continue
            if not constructor._valid_dependency(current_wheel_name, dependency.name()):
                continue
            if dependency.applies_to_target(target_platform):
                extracted_deps.add(dependency)
        return extracted_deps


def find_homepage(item: Message) -> str:
    homepage = str_from_message(item, "home-page")
    if homepage:
        return homepage
    else:
        return ""


def str_from_message(metadata: Message, key: str) -> Optional[str]:
    maybe_value = metadata.get(key)
    if isinstance(maybe_value, str):
        return maybe_value
    else:
        return None


def list_from_message(metadata: Message, key: str) -> Optional[List[str]]:
    maybe_value = metadata.get_all(key)
    if isinstance(maybe_value, list):
        return [str(item) if isinstance(item, Header) else item for item in maybe_value]
    else:
        return None


def find_release(wheel: Wheel, wheel_data: Dict[str, Any], logger: Logger) -> UrlSource:
    EXTENSIONS = [".tar.gz", ".tar.bz2", ".tar", ".zip", ".tgz"]

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
