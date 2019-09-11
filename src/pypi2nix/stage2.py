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
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.sources import Sources
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import TO_IGNORE
from pypi2nix.utils import cmd
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import safe
from pypi2nix.wheel import Wheel
from pypi2nix.wheel import find_release

INDEX_URL = "https://pypi.io/pypi"
INDEX_URL = "https://pypi.python.org/pypi"


class Stage2:
    def __init__(
        self,
        sources: Sources,
        verbose: int,
        logger: Logger,
        requirement_parser: RequirementParser,
        index: str = INDEX_URL,
    ) -> None:
        self.sources = sources
        self.verbose = verbose
        self.index = index
        self.logger = logger
        self.requirement_parser = requirement_parser

    def main(
        self,
        wheel_paths: Iterable[str],
        target_platform: TargetPlatform,
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
        for wheel_path in wheel_paths:

            self.logger.debug("|-> from %s" % os.path.basename(wheel_path))

            wheel_metadata = Wheel.from_wheel_directory_path(
                wheel_path, target_platform, self.logger, self.requirement_parser
            )
            if not wheel_metadata:
                continue

            if wheel_metadata.name in TO_IGNORE:
                self.logger.debug("    SKIPPING")
                continue
            if wheel_metadata.name in additional_dependencies:
                wheel_metadata.add_build_dependencies(
                    additional_dependencies[wheel_metadata.name]
                )

            wheels.append(wheel_metadata)

            self.logger.debug(
                "-- wheel_metadata --------------------------------------------------------"
            )
            self.logger.debug(
                json.dumps(wheel_metadata.to_dict(), sort_keys=True, indent=4)
            )
            self.logger.debug(
                "--------------------------------------------------------------------------"
            )

            self.process_wheel(wheel_metadata)
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
