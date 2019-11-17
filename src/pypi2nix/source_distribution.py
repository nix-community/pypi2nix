import email
import os
import os.path
from email.header import Header
from email.message import Message
from typing import Any
from typing import Iterable
from typing import Optional

from packaging.utils import canonicalize_name
from setuptools.config import read_configuration

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.package.interfaces import HasBuildDependencies
from pypi2nix.package.pyproject import PyprojectToml
from pypi2nix.requirement_parser import ParsingFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform


class DistributionNotDetected(Exception):
    pass


class SourceDistribution(HasBuildDependencies):
    def __init__(
        self,
        name: str,
        logger: Logger,
        requirement_parser: RequirementParser,
        pyproject_toml: Optional[PyprojectToml] = None,
        setup_cfg: Any = None,
    ) -> None:
        self.name = canonicalize_name(name)
        self.pyproject_toml = pyproject_toml
        self.setup_cfg = setup_cfg
        self.logger = logger
        self.requirement_parser = requirement_parser

    @classmethod
    def from_archive(
        source_distribution,
        archive: Archive,
        logger: Logger,
        requirement_parser: RequirementParser,
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
            name: str = metadata.get("name")
            if isinstance(name, Header):
                raise DistributionNotDetected(
                    "Could not parse source distribution metadata, name detection failed"
                )
            pyproject_toml = source_distribution.get_pyproject_toml(
                name, extracted_files, logger, requirement_parser
            )
            setup_cfg = source_distribution.get_setup_cfg(extracted_files)
        return source_distribution(
            name=name,
            pyproject_toml=pyproject_toml,
            setup_cfg=setup_cfg,
            logger=logger,
            requirement_parser=requirement_parser,
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
    def get_pyproject_toml(
        _,
        name: str,
        extracted_files: Iterable[str],
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> Optional[PyprojectToml]:
        pyproject_toml_candidates = [
            filepath
            for filepath in extracted_files
            if os.path.basename(filepath) == "pyproject.toml"
        ]
        if pyproject_toml_candidates:
            with open(pyproject_toml_candidates[0]) as f:
                content = f.read()
                return PyprojectToml(
                    name=name,
                    file_content=content,
                    requirement_parser=requirement_parser,
                    logger=logger,
                )
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

    def build_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        if self.pyproject_toml is not None:
            return self.build_dependencies_from_pyproject_toml(target_platform)
        elif self.setup_cfg is not None:
            return self.build_dependencies_from_setup_cfg(target_platform)
        else:
            return RequirementSet(target_platform)

    def build_dependencies_from_pyproject_toml(
        self, target_platform: TargetPlatform
    ) -> RequirementSet:
        if self.pyproject_toml is None:
            return RequirementSet(target_platform)
        else:
            return self.pyproject_toml.build_dependencies(target_platform)

    def build_dependencies_from_setup_cfg(
        self, target_platform: TargetPlatform
    ) -> RequirementSet:
        setup_requires = self.setup_cfg.get("options", {}).get("setup_requires")
        requirements = RequirementSet(target_platform)
        if isinstance(setup_requires, str):
            requirements.add(self.requirement_parser.parse(setup_requires))
        elif isinstance(setup_requires, list):
            for requirement_string in setup_requires:
                try:
                    requirement = self.requirement_parser.parse(requirement_string)
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
