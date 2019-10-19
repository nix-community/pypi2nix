import os
import os.path
import zipfile
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.pip.interface import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.source_distribution import DistributionNotDetected
from pypi2nix.source_distribution import SourceDistribution
from pypi2nix.target_platform import TargetPlatform


class WheelBuilder:
    def __init__(
        self,
        pip: Pip,
        project_directory: str,
        logger: Logger,
        requirement_parser: RequirementParser,
        target_platform: TargetPlatform,
    ) -> None:
        self.pip = pip
        self.download_directory = os.path.join(project_directory, "download")
        self.wheel_directory = os.path.join(project_directory, "wheel")
        self.extracted_wheels_directory = os.path.join(project_directory, "wheelhouse")
        self.project_directory = project_directory
        self.inspected_source_distribution_files: Set[str] = set()
        self.target_platform = target_platform
        self.additional_build_dependencies: Dict[str, RequirementSet] = defaultdict(
            lambda: RequirementSet(self.target_platform)
        )
        self.logger = logger
        self.requirement_parser = requirement_parser
        self.lib_directory = os.path.join(self.project_directory, "lib")

    def build(
        self,
        requirements: RequirementSet,
        setup_requirements: Optional[RequirementSet] = None,
    ) -> List[str]:
        self.ensure_download_directory_exists()
        if not setup_requirements:
            setup_requirements = RequirementSet(self.target_platform)
        else:
            self.logger.info("Installing setup requirements")
            setup_requirements = (
                self.detect_additional_build_dependencies(setup_requirements)
                + setup_requirements
            )
            self.pip.install(
                setup_requirements,
                target_directory=self.lib_directory,
                source_directories=[self.download_directory],
            )
        self.logger.info("Installing runtime requirements")
        requirements = requirements + setup_requirements
        detected_requirements = self.detect_additional_build_dependencies(requirements)
        updated_requirements = detected_requirements + requirements
        self.logger.info("Build wheels of setup and runtime requirements")
        self.pip.build_wheels(
            updated_requirements, self.wheel_directory, [self.download_directory]
        )
        return self.extract_wheels()

    def detect_additional_build_dependencies(
        self, requirements: RequirementSet, constraints: Optional[RequirementSet] = None
    ) -> RequirementSet:
        if constraints is None:
            constraints = RequirementSet(self.target_platform)
        self.pip.download_sources(
            requirements + constraints.to_constraints_only(), self.download_directory
        )
        uninspected_distributions = self.get_uninspected_source_distributions()
        self.register_all_source_distributions()
        detected_dependencies = RequirementSet(self.target_platform)
        if not uninspected_distributions:
            return detected_dependencies
        for distribution in uninspected_distributions:
            build_dependencies = distribution.build_dependencies(
                self.target_platform, self.requirement_parser
            ).filter(lambda requirement: requirement.name() not in [distribution.name])
            self.additional_build_dependencies[distribution.name] += build_dependencies
            detected_dependencies += build_dependencies
        return detected_dependencies + self.detect_additional_build_dependencies(
            detected_dependencies,
            constraints=(requirements + constraints).to_constraints_only(),
        )

    def get_uninspected_source_distributions(self) -> List[SourceDistribution]:
        archives = [
            Archive(path=path)
            for path in list_files(self.download_directory)
            if path not in self.inspected_source_distribution_files
        ]
        distributions = list()
        for archive in archives:
            try:
                distributions.append(
                    SourceDistribution.from_archive(archive, self.logger)
                )
            except DistributionNotDetected:
                continue
        return distributions

    def register_all_source_distributions(self) -> None:
        for path in list_files(self.download_directory):
            self.inspected_source_distribution_files.add(path)

    def extract_wheels(self) -> List[str]:
        self.ensure_extracted_wheels_directory_exists()

        wheels = [
            file_path
            for file_path in list_files(self.wheel_directory)
            if os.path.isfile(file_path) and file_path.endswith(".whl")
        ]
        for wheel in wheels:
            zip_file = zipfile.ZipFile(wheel)
            try:
                zip_file.extractall(self.extracted_wheels_directory)
            finally:
                zip_file.close()

        return [
            dist_info
            for dist_info in list_files(self.extracted_wheels_directory)
            if dist_info.endswith(".dist-info")
        ]

    def get_frozen_requirements(self) -> str:
        return self.pip.freeze(python_path=[self.extracted_wheels_directory])

    def ensure_download_directory_exists(self) -> None:
        try:
            os.makedirs(self.download_directory)
        except FileExistsError:
            pass

    def ensure_extracted_wheels_directory_exists(self) -> None:
        try:
            os.makedirs(self.extracted_wheels_directory)
        except FileExistsError:
            pass


def list_files(path: str) -> List[str]:
    return list(map(lambda f: os.path.join(path, f), os.listdir(path)))
