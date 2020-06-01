"""This module implements a class to collect requirements from command line arguments
given to pypi2nix
"""

import os.path

from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Logger
from pypi2nix.package_source import PathSource
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import PathRequirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources
from pypi2nix.target_platform import TargetPlatform


class RequirementsCollector:
    def __init__(
        self,
        platform: TargetPlatform,
        requirement_parser: RequirementParser,
        logger: Logger,
        project_directory: str,
        base_dependency_graph: DependencyGraph,
    ):
        self.platform = platform
        self.requirement_set = RequirementSet(platform)
        self.requirement_parser = requirement_parser
        self.logger = logger
        self._project_directory = project_directory
        self._sources = Sources()
        self._base_dependency_graph = base_dependency_graph

    def requirements(self) -> RequirementSet:
        return self.requirement_set

    def add_line(self, line: str) -> None:
        original_dependency = self.requirement_parser.parse(line)
        transitive_requirements = self._base_dependency_graph.get_all_build_dependency_names(
            original_dependency
        )
        self._add_line_without_dependency_check(line)
        for requirement in transitive_requirements:
            self._add_line_without_dependency_check(requirement)

    def add_file(self, file_path: str) -> None:
        requirements_file = RequirementsFile(
            file_path, self._project_directory, self.requirement_parser, self.logger
        )
        requirements_file.process()
        self._sources.update(requirements_file.sources())
        added_requirements = RequirementSet.from_file(
            requirements_file, self.platform, self.requirement_parser, self.logger
        )
        transitive_requirements = set()
        for requirement in added_requirements:
            transitive_requirements.update(
                self._base_dependency_graph.get_all_build_dependency_names(requirement)
            )
        for line in transitive_requirements:
            self._add_line_without_dependency_check(line)
        self.requirement_set += added_requirements

    def sources(self) -> Sources:
        sources = Sources()
        sources.update(self.requirement_set.sources())
        sources.update(self._sources)
        return sources

    def _add_line_without_dependency_check(self, line: str) -> None:
        requirement = self.requirement_parser.parse(line)
        if isinstance(requirement, PathRequirement):
            requirement = requirement.change_path(
                lambda path: self._handle_requirements_path(
                    name=requirement.name(), path=path
                )
            )
        self.requirement_set.add(requirement)

    def _handle_requirements_path(self, name: str, path: str) -> str:
        self._sources.add(name, PathSource(path))
        return os.path.abspath(path)
