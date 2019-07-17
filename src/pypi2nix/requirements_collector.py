"""This module implements a class to collect requirements from command line arguments
given to pypi2nix
"""

import os.path
import tempfile

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.requirements_file import RequirementsFile


class RequirementsCollector:
    def __init__(self, platform):
        self.platform = platform
        self.requirement_set = RequirementSet(platform)

    def requirements(self):
        return self.requirement_set

    def add_line(self, line):
        requirement = Requirement.from_line(line)
        if requirement.url:
            requirement.url = os.path.abspath(requirement.url)
        self.requirement_set.add(requirement)

    def add_file(self, file_path):
        with tempfile.TemporaryDirectory() as project_directory:
            requirements_file = RequirementsFile(file_path, project_directory)
            requirements_file.process()
            added_requirements = RequirementSet.from_file(
                requirements_file, self.platform
            )
        self.requirement_set += added_requirements
