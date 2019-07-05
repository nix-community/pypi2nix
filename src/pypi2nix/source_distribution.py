import email
import os
import tarfile
import tempfile

import toml

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement


class SourceDistribution:
    def __init__(self, name, pyproject_toml):
        self.name = name
        self.pyproject_toml = pyproject_toml

    @classmethod
    def from_tarball(source_distribution, tarball_path):
        with tempfile.TemporaryDirectory() as extraction_directory, tarfile.open(
            tarball_path, "r:gz"
        ) as tar:
            tar.extractall(path=extraction_directory)
            extracted_files = [
                os.path.join(directory_path, file_name)
                for directory_path, _, file_names in os.walk(extraction_directory)
                for file_name in file_names
            ]
            metadata = source_distribution.metadata_from_uncompressed_distribution(
                extracted_files
            )
            pyproject_toml = source_distribution.get_pyproject_toml(extracted_files)
        return source_distribution(
            name=metadata.get("name"), pyproject_toml=pyproject_toml
        )

    @classmethod
    def metadata_from_uncompressed_distribution(_, extracted_files):
        pkg_info_files = [
            filepath for filepath in extracted_files if filepath.endswith("PKG-INFO")
        ]
        assert pkg_info_files
        pkg_info_file = pkg_info_files[0]
        with open(pkg_info_file) as f:
            metadata = email.parser.Parser().parse(f)
        return metadata

    @classmethod
    def get_pyproject_toml(_, extracted_files):
        pyproject_toml_candidates = [
            filepath
            for filepath in extracted_files
            if filepath.endswith("pyproject.toml")
        ]
        if pyproject_toml_candidates:
            with open(pyproject_toml_candidates[0]) as f:
                return toml.load(f)
        else:
            return None

    def build_dependencies(self):
        requirement_set = RequirementSet()
        if self.pyproject_toml is None:
            pass
        else:
            for build_input in self.pyproject_toml.get("build-system", {}).get(
                "requires", []
            ):
                requirement = Requirement.from_line(build_input)
                if requirement.applies_to_system():
                    requirement_set.add(requirement)
        return requirement_set
