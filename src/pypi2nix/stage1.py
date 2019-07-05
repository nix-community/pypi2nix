import os
import os.path
import zipfile

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.source_distribution import SourceDistribution


class WheelBuilder:
    def __init__(self, pip, project_directory):
        self.pip = pip
        self.download_directory = os.path.join(project_directory, "download")
        self.wheel_directory = os.path.join(project_directory, "wheel")
        self.extracted_wheels_directory = os.path.join(project_directory, "wheelhouse")
        self.project_directory = project_directory
        self.indexes = [self.wheel_directory]
        self.deps = dict()
        self.inspected_source_distribution_files = set()

    def build(self, requirements, setup_requirements=RequirementSet()):
        requirements = requirements + setup_requirements
        updated_requirements = self.detect_additional_build_dependencies(requirements)
        self.pip.build_wheels(
            updated_requirements, self.wheel_directory, [self.download_directory]
        )
        return self.extract_wheels()

    def detect_additional_build_dependencies(self, requirements):
        self.pip.download_sources(requirements, self.download_directory)
        uninspected_distributions = self.get_uninspected_source_distributions()
        self.register_all_source_distributions()
        detected_dependencies = RequirementSet() + requirements
        if not uninspected_distributions:
            return detected_dependencies
        for distribution in uninspected_distributions:
            detected_dependencies += distribution.build_dependencies()
        return detected_dependencies + self.detect_additional_build_dependencies(
            detected_dependencies
        )

    def get_uninspected_source_distributions(self):
        return list(
            map(
                SourceDistribution.from_tarball,
                filter(
                    lambda path: path not in self.inspected_source_distribution_files,
                    list_files(self.download_directory),
                ),
            )
        )

    def register_all_source_distributions(self):
        for path in list_files(self.download_directory):
            self.inspected_source_distribution_files.add(path)

    def extract_wheels(self):
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

    def get_frozen_requirements(self):
        return self.pip.freeze(python_path=[self.extracted_wheels_directory])

    def ensure_download_directory_exists(self):
        try:
            os.makedirs(self.download_directory)
        except FileExistsError:
            pass

    def ensure_extracted_wheels_directory_exists(self):
        try:
            os.makedirs(self.extracted_wheels_directory)
        except FileExistsError:
            pass


def list_files(path):
    return map(lambda f: os.path.join(path, f), os.listdir(path))
