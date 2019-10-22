import email
import os
import os.path
from email.header import Header
from email.message import Message
from typing import Any
from typing import Iterable

import toml
from packaging.utils import canonicalize_name
from setuptools.config import read_configuration

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import ParsingFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform


class DistributionNotDetected(Exception):
    pass


class SourceDistribution:
    def __init__(
        self,
        name: str,
        logger: Logger,
        pyproject_toml: Any = None,
        setup_cfg: Any = None,
    ) -> None:
        self.name = canonicalize_name(name)
        self.pyproject_toml = pyproject_toml
        self.setup_cfg = setup_cfg
        self.logger = logger

    @classmethod
    def from_archive(
        source_distribution, archive: Archive, logger: Logger
    ) -> "SourceDistribution":
        with archive.extracted_files() as extraction_directory:
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
        name = metadata.get("name")
        if isinstance(name, Header):
            raise DistributionNotDetected(
                "Could not parse source distribution metadata, name detection failed"
            )
        return source_distribution(
            name=name, pyproject_toml=pyproject_toml, setup_cfg=setup_cfg, logger=logger
        )

    @classmethod
    def metadata_from_uncompressed_distribution(
        _, extracted_files: Iterable[str], archive: Archive
    ) -> Message:
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
    def get_pyproject_toml(_, extracted_files: Iterable[str]) -> Any:
        pyproject_toml_candidates = [
            filepath
            for filepath in extracted_files
            if os.path.basename(filepath) == "pyproject.toml"
        ]
        if pyproject_toml_candidates:
            with open(pyproject_toml_candidates[0]) as f:
                return toml.load(f)
        else:
            return None

    @classmethod
    def get_setup_cfg(_, extracted_files: Iterable[str]) -> Any:
        setup_cfg_candidates = [
            filepath
            for filepath in extracted_files
            if os.path.basename(filepath) == "setup.cfg"
        ]
        if setup_cfg_candidates:
            return read_configuration(setup_cfg_candidates[0])

    def build_dependencies(
        self, target_platform: TargetPlatform, requirement_parser: RequirementParser
    ) -> RequirementSet:
        if self.pyproject_toml is not None:
            return self.build_dependencies_from_pyproject_toml(
                target_platform, requirement_parser
            )
        elif self.setup_cfg is not None:
            return self.build_dependencies_from_setup_cfg(
                target_platform, requirement_parser
            )
        else:
            return RequirementSet(target_platform)

    def build_dependencies_from_pyproject_toml(
        self, target_platform: TargetPlatform, requirement_parser: RequirementParser
    ) -> RequirementSet:
        requirement_set = RequirementSet(target_platform)
        if self.pyproject_toml is None:
            pass
        else:
            for build_input in self.pyproject_toml.get("build-system", {}).get(
                "requires", []
            ):
                try:
                    requirement = requirement_parser.parse(build_input)
                except ParsingFailed as e:
                    self.logger.warning(
                        "Failed to parse build dependency of `{name}`".format(
                            name=self.name
                        )
                    )
                    self.logger.warning(
                        "Possible reason: `{reason}`".format(reason=e.reason)
                    )
                else:
                    if requirement.applies_to_target(target_platform):
                        requirement_set.add(requirement)
        return requirement_set

    def build_dependencies_from_setup_cfg(
        self, target_platform: TargetPlatform, requirement_parser: RequirementParser
    ) -> RequirementSet:
        setup_requires = self.setup_cfg.get("options", {}).get("setup_requires")
        requirements = RequirementSet(target_platform)
        if isinstance(setup_requires, str):
            requirements.add(requirement_parser.parse(setup_requires))
        elif isinstance(setup_requires, list):
            for requirement_string in setup_requires:
                try:
                    requirement = requirement_parser.parse(requirement_string)
                except ParsingFailed as e:
                    self.logger.warning(
                        "Failed to parse build dependency of `{name}`".format(
                            name=self.name
                        )
                    )
                    self.logger.warning(
                        "Possible reason: `{reason}`".format(reason=e.reason)
                    )
                else:
                    if requirement.applies_to_target(target_platform):
                        requirements.add(requirement)
        return requirements
