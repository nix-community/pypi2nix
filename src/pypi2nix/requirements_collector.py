"""This module implements a class to collect requirements from command line arguments
given to pypi2nix
"""

import os.path
import tempfile

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import PathRequirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.target_platform import TargetPlatform


class RequirementsCollector:
    def __init__(
        self,
        platform: TargetPlatform,
        requirement_parser: RequirementParser,
        logger: Logger,
    ):
        self.platform = platform
        self.requirement_set = RequirementSet(platform)
        self.requirement_parser = requirement_parser
        self.logger = logger

    def requirements(self) -> RequirementSet:
        return self.requirement_set

    def add_line(self, line: str) -> None:
        requirement = self.requirement_parser.parse(line)
        if isinstance(requirement, PathRequirement):
            requirement = requirement.change_path(os.path.abspath)
        self.requirement_set.add(requirement)

    def add_file(self, file_path: str) -> None:
        with tempfile.TemporaryDirectory() as project_directory:
            requirements_file = RequirementsFile(
                file_path, project_directory, self.requirement_parser, self.logger
            )
            requirements_file.process()
            added_requirements = RequirementSet.from_file(
                requirements_file, self.platform, self.requirement_parser, self.logger
            )
        self.requirement_set += added_requirements
