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
from urllib.request import urlopen

import click

from pypi2nix.logger import Logger
from pypi2nix.package_source import UrlSource
from pypi2nix.pypi import Pypi
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.sources import Sources
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import cmd
from pypi2nix.utils import prefetch_git
from pypi2nix.utils import safe
from pypi2nix.wheel import Wheel


class Stage2:
    def __init__(
        self,
        sources: Sources,
        logger: Logger,
        requirement_parser: RequirementParser,
        pypi: Pypi,
    ) -> None:
        self.sources = sources
        self.logger = logger
        self.requirement_parser = requirement_parser
        self.pypi = pypi

    def main(
        self,
        wheel_paths: Iterable[str],
        target_platform: TargetPlatform,
        additional_dependencies: Dict[str, RequirementSet],
    ) -> List[Wheel]:
        """Extract packages metadata from wheels dist-info folders.
        """
        output = ""
        metadata: List[Wheel] = []

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

    def process_wheel(self, wheel: Wheel) -> None:
        if wheel.name not in self.sources:
            release = self.pypi.get_source_release(wheel.name, wheel.version)
            if release:
                source = UrlSource(
                    url=release.url,
                    logger=self.logger,
                    hash_value=release.sha256_digest,
                )
                self.sources.add(wheel.name, source)
            else:
                self.logger.error(
                    f"Failed to query pypi for release name=`{wheel.name}`, version=`{wheel.version}`"
                )
                raise MetadataFetchingFailed()


class MetadataFetchingFailed(Exception):
    pass
