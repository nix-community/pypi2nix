import email.parser
import os.path
from email.header import Header
from email.message import Message
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Type

import click
import setuptools._vendor.packaging.requirements
from setuptools._vendor.packaging.utils import canonicalize_name

from pypi2nix.license import find_license
from pypi2nix.utils import TO_IGNORE
from pypi2nix.utils import safe


class Wheel:
    def __init__(
        self,
        name: str,
        version: str,
        deps: Iterable[str],
        homepage: str,
        license: str,
        description: str,
        build_dependencies: Set[str] = set(),
    ):
        self.name = canonicalize_name(name)
        self.version = version
        self.deps = set(map(canonicalize_name, deps))
        self.homepage = homepage
        self.license = license
        self.description = description
        self.build_dependencies = set(map(canonicalize_name, build_dependencies))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "deps": list(self.deps),
            "homepage": self.homepage,
            "license": self.license,
            "description": self.description,
            "build_dependencies": list(self.build_dependencies),
        }

    def add_build_dependencies(self, dependencies: Iterable[str]) -> None:
        for dependency in dependencies:
            if self.valid_dependency(dependency):
                self.build_dependencies.add(canonicalize_name(dependency))

    def valid_dependency(self, dependency: str) -> bool:
        canonicalized_dependency = canonicalize_name(dependency)
        return all(
            [
                canonicalized_dependency != self.name,
                canonicalized_dependency not in TO_IGNORE,
            ]
        )

    @classmethod
    def from_wheel_directory_path(
        wheel_class: "Type[Wheel]",
        wheel_directory_path: str,
        default_environment: Dict[str, Any],
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
                click.echo(
                    "WARNING: Couldn't recognize license `{}` for `{}`".format(
                        license_string, metadata.get("name")
                    )
                )

            name = str_from_message(metadata, "name")
            if name is None:
                raise Exception("Could not extract name from wheel metadata")

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
                deps=extract_deps(dependencies, default_environment),
                homepage=safe(find_homepage(metadata)),
                license=license,
                description=safe(description),
            )

        raise click.ClickException(
            "Unable to find METADATA in `%s` folder." % wheel_directory_path
        )


def extract_deps(deps: Iterable[str], default_environment: Dict[str, Any]) -> List[str]:
    """Get dependent packages from metadata.

    Note that this is currently very rough stuff. I consider only the
    first 'requires' dataset in 'run_requires'. Other requirement sets
    like 'test_requires' are completely ignored.
    """
    extracted_deps = []
    for dep in deps:
        req = setuptools._vendor.packaging.requirements.Requirement(dep)

        if req.name.lower() in TO_IGNORE:
            continue

        if req.marker:

            extra = None
            for marker in req.marker._markers:
                if len(marker) != 3:
                    continue
                if (
                    type(marker[0]) == setuptools._vendor.packaging.markers.Variable
                    and type(marker[1]) == setuptools._vendor.packaging.markers.Op
                    and type(marker[2]) == setuptools._vendor.packaging.markers.Value
                    and marker[0].value == "extra"
                    and marker[1].value == "=="
                ):
                    extra = marker[2].value
                    break

            if extra:
                # this will save us from some cyclic dependencies until we have
                # time to implement real solution
                if extra in ["test", "tests", "dev", "docs", "doc"]:
                    continue
                environment = dict(**default_environment, **dict(extra=extra))
            else:
                environment = dict(**default_environment)

            if not req.marker.evaluate(environment):
                continue

        extracted_deps.append(req.name)

    return list(set(extracted_deps))


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
