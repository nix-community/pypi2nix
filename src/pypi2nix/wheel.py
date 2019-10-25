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
from packaging.utils import canonicalize_name

from pypi2nix.license import find_license
from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform
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
        target_platform: TargetPlatform,
    ):
        self.name = canonicalize_name(name)
        self.version = version
        self._deps = deps
        self.homepage = homepage
        self.license = license
        self.description = description
        self.build_dependencies: RequirementSet = build_dependencies
        self._target_platform = target_platform

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "deps": [requirement.name() for requirement in self._deps],
            "homepage": self.homepage,
            "license": self.license,
            "description": self.description,
            "build_dependencies": [
                requirement.name() for requirement in self.build_dependencies
            ],
        }

    def dependencies(self, extras: List[str] = []) -> RequirementSet:
        return self._deps.filter(
            lambda requirement: requirement.applies_to_target(
                self._target_platform, extras=extras
            )
        )

    def add_build_dependencies(self, dependencies: RequirementSet) -> None:
        self.build_dependencies += dependencies

    @classmethod
    def _valid_dependency(constructor, name: str, dependency: str) -> bool:
        canonicalized_dependency = canonicalize_name(dependency)
        return canonicalized_dependency != name

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
            classifiers = list_from_message(metadata, "Classifier")
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
                target_platform=target_platform,
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
            if not constructor._valid_dependency(current_wheel_name, dependency.name()):
                continue
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
