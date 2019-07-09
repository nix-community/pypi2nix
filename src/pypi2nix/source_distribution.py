import email
import os

import setupcfg
import toml
from setuptools._vendor.packaging.utils import canonicalize_name

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement


class DistributionNotDetected(Exception):
    pass


class SourceDistribution:
    def __init__(self, name, pyproject_toml=None, setup_cfg=None):
        self.name = canonicalize_name(name)
        self.pyproject_toml = pyproject_toml
        self.setup_cfg = setup_cfg

    @classmethod
    def from_archive(source_distribution, archive):
        with archive.contents() as extraction_directory:
            extracted_files = [
                os.path.join(directory_path, file_name)
                for directory_path, _, file_names in os.walk(extraction_directory)
                for file_name in file_names
            ]
            metadata = source_distribution.metadata_from_uncompressed_distribution(
                extracted_files, archive
            )
            pyproject_toml = source_distribution.get_pyproject_toml(extracted_files)
            setup_cfg = source_distribution.get_setup_cfg(extracted_files)
        return source_distribution(
            name=metadata.get("name"),
            pyproject_toml=pyproject_toml,
            setup_cfg=setup_cfg,
        )

    @classmethod
    def metadata_from_uncompressed_distribution(_, extracted_files, archive):
        pkg_info_files = [
            filepath for filepath in extracted_files if filepath.endswith("PKG-INFO")
        ]
        if not pkg_info_files:
            raise DistributionNotDetected(
                "`{}` does not appear to be a python source distribution, Could not find PKG-INFO file".format(
                    archive.path
                )
            )
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

    @classmethod
    def get_setup_cfg(_, extracted_files):
        setup_cfg_candidates = [
            filepath for filepath in extracted_files if filepath.endswith("setup.cfg")
        ]
        if setup_cfg_candidates:
            return setupcfg.load(setup_cfg_candidates)

    def build_dependencies(self, target_platform):
        if self.pyproject_toml is not None:
            return self.build_dependencies_from_pyproject_toml(target_platform)
        elif self.setup_cfg is not None:
            return self.build_dependencies_from_setup_cfg(target_platform)
        else:
            return RequirementSet()

    def build_dependencies_from_pyproject_toml(self, target_platform):
        requirement_set = RequirementSet()
        if self.pyproject_toml is None:
            pass
        else:
            for build_input in self.pyproject_toml.get("build-system", {}).get(
                "requires", []
            ):
                requirement = Requirement.from_line(build_input)
                if requirement.applies_to_target(target_platform):
                    requirement_set.add(requirement)
        return requirement_set

    def build_dependencies_from_setup_cfg(self, target_platform):
        setup_requires = self.setup_cfg.get("options", {}).get("setup_requires")
        requirements = RequirementSet()
        if isinstance(setup_requires, str):
            requirements.add(Requirement.from_line(setup_requires))
        elif isinstance(setup_requires, list):
            for requirement_string in setup_requires:
                requirement = Requirement.from_line(requirement_string)
                if requirement.applies_to_target(target_platform):
                    requirements.add(requirement)
        return requirements
