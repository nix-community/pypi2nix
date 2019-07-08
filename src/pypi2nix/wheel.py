import email
import os.path

import click
import setuptools._vendor.packaging.requirements
from setuptools._vendor.packaging.utils import canonicalize_name

from pypi2nix.license import find_license
from pypi2nix.utils import TO_IGNORE
from pypi2nix.utils import safe


class Wheel:
    def __init__(
        self,
        name,
        version,
        deps,
        homepage,
        license,
        description,
        build_dependencies=set(),
    ):
        self.name = canonicalize_name(name)
        self.version = version
        self.deps = set(map(canonicalize_name, deps))
        self.homepage = homepage
        self.license = license
        self.description = description
        self.build_dependencies = set(map(canonicalize_name, build_dependencies))

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "deps": list(self.deps),
            "homepage": self.homepage,
            "license": self.license,
            "description": self.description,
            "build_dependencies": list(self.build_dependencies),
        }

    def add_build_dependencies(self, dependencies):
        for dependency in dependencies:
            self.build_dependencies.add(canonicalize_name(dependency))

    @classmethod
    def from_wheel_directory_path(
        wheel_class, wheel_directory_path, default_environment
    ):
        metadata_file = os.path.join(wheel_directory_path, "METADATA")
        if os.path.exists(metadata_file):
            with open(
                metadata_file, "r", encoding="ascii", errors="surrogateescape"
            ) as headers:
                metadata = email.parser.Parser().parse(headers)
            license_string = metadata.get("license", "")
            license = find_license(
                classifiers=metadata.get("classifiers", []),
                license_string=license_string,
            )

            if license is None:
                license = '"' + safe(license_string) + '"'
                click.echo(
                    "WARNING: Couldn't recognize license `{}` for `{}`".format(
                        license_string, metadata.get("name")
                    )
                )

            return wheel_class(
                **{
                    "name": metadata["name"],
                    "version": metadata["version"],
                    "deps": extract_deps(
                        metadata.get_all("requires-dist", []), default_environment
                    ),
                    "homepage": safe(find_homepage(metadata)),
                    "license": license,
                    "description": safe(metadata.get("summary", "")),
                }
            )

        raise click.ClickException(
            "Unable to find METADATA in `%s` folder." % wheel_directory_path
        )


def extract_deps(deps, default_environment):
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


def find_homepage(item):
    homepage = ""
    if (
        "extensions" in item
        and "python.details" in item["extensions"]
        and "project_urls" in item["extensions"]["python.details"]
    ):
        homepage = item["extensions"]["python.details"]["project_urls"].get("Home", "")
    elif "home-page" in item:
        homepage = item["home-page"]
    return homepage
