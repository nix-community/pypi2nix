import zipfile
from copy import copy
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from pypi2nix.archive import Archive
from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Logger
from pypi2nix.package import DistributionNotDetected
from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.source_distribution import SourceDistribution
from pypi2nix.target_platform import TargetPlatform


class WheelBuilder:
    def __init__(
        self,
        pip: Pip,
        download_directory: Path,
        wheel_directory: Path,
        extracted_wheel_directory: Path,
        lib_directory: Path,
        logger: Logger,
        requirement_parser: RequirementParser,
        target_platform: TargetPlatform,
        base_dependency_graph: DependencyGraph,
    ) -> None:
        self.pip = pip
        self._download_directory = download_directory
        self._wheel_directory = wheel_directory
        self._extracted_wheels_directory: Path = extracted_wheel_directory
        self.inspected_source_distribution_files: Set[Path] = set()
        self.target_platform = target_platform
        self.source_distributions: Dict[str, SourceDistribution] = dict()
        self.logger = logger
        self.requirement_parser = requirement_parser
        self.lib_directory = lib_directory
        self._dependency_graph = base_dependency_graph

    def build(
        self,
        requirements: RequirementSet,
        setup_requirements: Optional[RequirementSet] = None,
    ) -> List[str]:
        self.ensure_download_directory_exists()
        self._ensure_wheels_directory_exists()
        if not setup_requirements:
            setup_requirements = RequirementSet(self.target_platform)
        else:
            self.logger.info("Downloading setup requirements")
            setup_requirements = (
                self.detect_additional_build_dependencies(setup_requirements)
                + setup_requirements
            )
            self.logger.info("Installing setup requirements")
            self.pip.install(
                setup_requirements,
                target_directory=self.lib_directory,
                source_directories=[self._download_directory],
            )
        self.logger.info("Downloading runtime requirements")
        requirements = requirements + setup_requirements
        detected_requirements = self.detect_additional_build_dependencies(requirements)
        updated_requirements = detected_requirements + requirements
        self.logger.info("Build wheels of setup and runtime requirements")
        self.pip.build_wheels(
            updated_requirements, self._wheel_directory, [self._download_directory],
        )
        return self.extract_wheels()

    def detect_additional_build_dependencies(
        self, requirements: RequirementSet, constraints: Optional[RequirementSet] = None
    ) -> RequirementSet:
        if constraints is None:
            constraints = RequirementSet(self.target_platform)
        self.pip.download_sources(
            requirements + constraints.to_constraints_only(), self._download_directory,
        )
        uninspected_distributions = self.get_uninspected_source_distributions()
        self.register_all_source_distributions()
        detected_dependencies = RequirementSet(self.target_platform)
        if not uninspected_distributions:
            return detected_dependencies
        for distribution in uninspected_distributions:
            detected_dependencies += self._get_build_dependencies_for_distribution(
                distribution
            )
        return detected_dependencies + self.detect_additional_build_dependencies(
            detected_dependencies,
            constraints=(requirements + constraints).to_constraints_only(),
        )

    def _get_build_dependencies_for_distribution(
        self, distribution: SourceDistribution
    ) -> RequirementSet:
        self.source_distributions[distribution.name] = distribution
        build_dependencies = distribution.build_dependencies(
            self.target_platform
        ).filter(lambda requirement: requirement.name() not in [distribution.name])
        for dependency in build_dependencies:
            self._dependency_graph.set_buildtime_dependency(
                dependent=distribution.to_loose_requirement(), dependency=dependency
            )
        return build_dependencies

    def get_uninspected_source_distributions(self) -> List[SourceDistribution]:
        archives = [
            Archive(path=str(path))
            for path in self._download_directory.list_files()
            if path not in self.inspected_source_distribution_files
        ]
        distributions = list()
        for archive in archives:
            try:
                distribution = SourceDistribution.from_archive(
                    archive, self.logger, requirement_parser=self.requirement_parser
                )
            except DistributionNotDetected:
                continue
            distributions.append(distribution)
        return distributions

    def register_all_source_distributions(self) -> None:
        for path in self._download_directory.list_files():
            self.inspected_source_distribution_files.add(path)

    def extract_wheels(self) -> List[str]:
        self.ensure_extracted_wheels_directory_exists()

        wheels = [
            str(file_path)
            for file_path in self._wheel_directory.list_files()
            if file_path.is_file() and str(file_path).endswith(".whl")
        ]
        for wheel in wheels:
            zip_file = zipfile.ZipFile(wheel)
            try:
                zip_file.extractall(str(self._extracted_wheels_directory))
            finally:
                zip_file.close()

        return [
            str(dist_info)
            for dist_info in self._extracted_wheels_directory.list_files()
            if str(dist_info).endswith(".dist-info")
        ]

    def get_frozen_requirements(self) -> str:
        return self.pip.freeze(python_path=[self._extracted_wheels_directory])

    def ensure_download_directory_exists(self) -> None:
        self._download_directory.ensure_directory()

    def ensure_extracted_wheels_directory_exists(self) -> None:
        self._extracted_wheels_directory.ensure_directory()

    def _ensure_wheels_directory_exists(self) -> None:
        self._wheel_directory.ensure_directory()

    @property
    def dependency_graph(self) -> DependencyGraph:
        return copy(self._dependency_graph)
