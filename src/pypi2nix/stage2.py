"""Parse metadata from .dist-info directories in a wheelhouse."""
# flake8: noqa: E501

import email
import hashlib
import json
import os.path
import tempfile
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List

import click
import requests

from pypi2nix.logger import Logger
from pypi2nix.package_source import find_release
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.sources import Sources
from pypi2nix.utils import TO_IGNORE
from pypi2nix.utils import cmd
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import safe
from pypi2nix.wheel import Wheel

INDEX_URL = "https://pypi.io/pypi"
INDEX_URL = "https://pypi.python.org/pypi"


class Stage2:
    def __init__(
        self, sources: Sources, verbose: int, logger: Logger, index: str = INDEX_URL
    ) -> None:
        self.sources = sources
        self.verbose = verbose
        self.index = index
        self.logger = logger

    def main(
        self,
        wheel_paths: Iterable[str],
        default_environment: Any,
        wheel_cache_dir: str,
        additional_dependencies: Dict[str, RequirementSet],
    ) -> List[Wheel]:
        """Extract packages metadata from wheels dist-info folders.
        """
        output = ""
        metadata: List[Wheel] = []

        if self.verbose > 1:
            self.logger.info(
                "-- sources ---------------------------------------------------------------"
            )
            for name, source in self.sources.items():
                self.logger.info("{name}, {source}".format(name=name, source=name))
            self.logger.info(
                "--------------------------------------------------------------------------"
            )

        wheels = []
        try:
            for wheel_path in wheel_paths:

                output += "|-> from %s" % os.path.basename(wheel_path)
                if self.verbose > 0:
                    click.echo("|-> from %s" % os.path.basename(wheel_path))

                wheel_metadata = Wheel.from_wheel_directory_path(
                    wheel_path, default_environment
                )
                if not wheel_metadata:
                    continue

                if wheel_metadata.name in TO_IGNORE:
                    if self.verbose > 0:
                        click.echo("    SKIPPING")
                    continue
                if wheel_metadata.name in additional_dependencies:
                    wheel_metadata.add_build_dependencies(
                        map(
                            lambda dependency: dependency.name(),
                            additional_dependencies[wheel_metadata.name],
                        )
                    )

                wheels.append(wheel_metadata)

                if self.verbose > 1:
                    click.echo(
                        "-- wheel_metadata --------------------------------------------------------"
                    )
                    click.echo(
                        json.dumps(wheel_metadata.to_dict(), sort_keys=True, indent=4)
                    )
                    click.echo(
                        "--------------------------------------------------------------------------"
                    )

                self.process_wheel(wheel_metadata)
        except Exception as e:
            if self.verbose == 0:
                click.echo(output)
            raise

        return wheels

    def process_wheel(self, wheel: Wheel, chunk_size: int = 2048) -> None:
        if wheel.name not in self.sources:
            url = "{}/{}/json".format(self.index, wheel.name)
            r = requests.get(url, timeout=None)
            r.raise_for_status()  # TODO: handle this nicer
            wheel_data = r.json()

            if not wheel_data.get("releases"):
                raise click.ClickException(
                    "Unable to find releases for packge {name}".format(name=wheel.name)
                )

            self.sources.add(wheel.name, find_release(wheel, wheel_data, self.logger))
