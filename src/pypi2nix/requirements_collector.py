"""This module implements a class to collect requirements from command line arguments
given to pypi2nix
"""

import os.path
import tempfile

from pypi2nix.requirement_parser import requirement_parser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import PathRequirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.target_platform import TargetPlatform


class RequirementsCollector:
    def __init__(self, platform: TargetPlatform):
        self.platform = platform
        self.requirement_set = RequirementSet(platform)

    def requirements(self) -> RequirementSet:
        return self.requirement_set

    def add_line(self, line: str) -> None:
        requirement = requirement_parser.parse(line)
        if isinstance(requirement, PathRequirement):
            requirement = requirement.change_path(os.path.abspath)
        self.requirement_set.add(requirement)

    def add_file(self, file_path: str) -> None:
        with tempfile.TemporaryDirectory() as project_directory:
            requirements_file = RequirementsFile(file_path, project_directory)
            requirements_file.process()
            added_requirements = RequirementSet.from_file(
                requirements_file, self.platform
            )
        self.requirement_set += added_requirements
