import email.parser
import os.path
from email.header import Header
from email.message import Message
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import click
from packaging.utils import canonicalize_name

from pypi2nix.license import find_license
from pypi2nix.logger import Logger
from pypi2nix.nix_language import escape_string
from pypi2nix.package import HasBuildDependencies
from pypi2nix.package import HasRuntimeDependencies
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform


class Wheel(HasRuntimeDependencies, HasBuildDependencies):
    def __init__(
        self,
        name: str,
        version: str,
        deps: RequirementSet,
        homepage: str,
        license: str,
        description: str,
        build_dependencies: RequirementSet,
        target_platform: TargetPlatform,
    ):
        self.name = canonicalize_name(name)
        self.version = version
        self._deps = deps
        self.homepage = homepage
        self.license = license
        self.description = description
        self._build_dependencies: RequirementSet = build_dependencies
        self._target_platform = target_platform
        self.package_format: str = "setuptools"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "deps": [requirement.name() for requirement in self._deps],
            "homepage": self.homepage,
            "license": self.license,
            "description": self.description,
            "build_dependencies": [
                requirement.name() for requirement in self._build_dependencies
            ],
        }

    def build_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        if target_platform != self._target_platform:
            return RequirementSet(target_platform)
        else:
            return self._build_dependencies

    def runtime_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        if target_platform != self._target_platform:
            return RequirementSet(target_platform)
        else:
            return self.dependencies([])

    def dependencies(self, extras: List[str] = []) -> RequirementSet:
        return self._deps.filter(
            lambda requirement: requirement.applies_to_target(
                self._target_platform, extras=extras
            )
        )

    def add_build_dependencies(self, dependencies: RequirementSet) -> None:
        self._build_dependencies += dependencies

    @classmethod
    def from_wheel_directory_path(
        wheel_class,
        wheel_directory_path: str,
        target_platform: TargetPlatform,
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> "Wheel":
        builder = Builder(
            target_platform, wheel_directory_path, logger, requirement_parser
        )
        return builder.build()

    def target_platform(self) -> TargetPlatform:
        return self._target_platform


class Builder:
    def __init__(
        self,
        target_platform: TargetPlatform,
        wheel_directory_path: str,
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> None:
        self.name: Optional[str] = None
        self.version: Optional[str] = None
        self.target_platform = target_platform
        self.runtime_dependencies: RequirementSet = RequirementSet(target_platform)
        self.homepage: Optional[str] = None
        self.license: Optional[str] = None
        self.description: Optional[str] = None
        self.build_dependencies = RequirementSet(target_platform)
        self.wheel_directory_path: str = wheel_directory_path
        self.logger = logger
        self.requirement_parser = requirement_parser
        self.pkg_info: Message = self._parse_pkg_info()

    def build(self) -> "Wheel":
        self._get_name()
        self._get_version()
        self._get_runtime_dependencies()
        self._get_homepage()
        self._get_license()
        self._get_description()
        return self._verify_integrity()

    def _verify_integrity(self) -> "Wheel":
        if self.version is None:
            raise Exception(
                f"Could not extract version from wheel metadata for `{self.name}`"
            )
        if self.name is None:
            raise Exception(
                f"Could not extract name info from metadata for package at `{self.wheel_directory_path}`"
            )
        if self.homepage is None:
            raise Exception(
                f"Could not extract homepage information from metadata for package `{self.name}`"
            )
        if self.license is None:
            raise Exception(
                f"Could not extract license information from metadata for package `{self.name}`"
            )
        if self.description is None:
            raise Exception(
                f"Could not extract description from metadata for package `{self.name}`"
            )
        return Wheel(
            name=self.name,
            version=self.version,
            target_platform=self.target_platform,
            deps=self.runtime_dependencies,
            build_dependencies=self.build_dependencies,
            homepage=self.homepage,
            license=self.license,
            description=self.description,
        )

    def _parse_pkg_info(self) -> Message:
        metadata_file = os.path.join(self.wheel_directory_path, "METADATA")
        if os.path.exists(metadata_file):
            with open(
                metadata_file, "r", encoding="ascii", errors="surrogateescape"
            ) as headers:
                return email.parser.Parser().parse(headers)
        else:
            raise click.ClickException(
                f"Unable to find METADATA in `{self.wheel_directory_path}` folder."
            )

    def _get_name(self) -> None:
        self.name = str_from_message(self.pkg_info, "name")
        if self.name is None:
            raise Exception(
                f"Could not extract name from wheel metadata at {self.wheel_directory_path}"
            )
        self.name = canonicalize_name(self.name)

    def _get_version(self) -> None:
        self.version = str_from_message(self.pkg_info, "version")

    def _get_license(self) -> None:
        license_string = str_from_message(self.pkg_info, "license")
        if license_string is None:
            license_string = ""
        classifiers = list_from_message(self.pkg_info, "Classifier")
        if classifiers is None:
            classifiers = []
        self.license = find_license(
            classifiers=classifiers, license_string=license_string
        )

        if self.license is None:
            self.license = '"' + escape_string(license_string) + '"'
            self.logger.warning(
                f"Couldn't recognize license `{license_string}` for `{self.name}`"
            )

    def _get_description(self) -> None:
        self.description = str_from_message(self.pkg_info, "summary")
        if self.description is None:
            self.description = ""

    def _get_runtime_dependencies(self) -> None:
        dependencies = list_from_message(self.pkg_info, "requires-dist")
        if dependencies is None:
            dependencies = []
        for dep_string in dependencies:
            dependency = self.requirement_parser.parse(dep_string)
            if not self._is_valid_dependency(dependency.name()):
                continue
            self.runtime_dependencies.add(dependency)

    def _is_valid_dependency(self, dependency_name: str) -> bool:
        canonicalized_dependency = canonicalize_name(dependency_name)
        return canonicalized_dependency != self.name

    def _get_homepage(self) -> None:
        self.homepage = str_from_message(self.pkg_info, "home-page")
        if not self.homepage:
            self.homepage = ""


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
