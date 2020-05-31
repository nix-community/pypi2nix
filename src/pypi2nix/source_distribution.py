import os
import os.path
from typing import Iterable
from typing import Optional

from packaging.utils import canonicalize_name

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.package import DistributionNotDetected
from pypi2nix.package import HasBuildDependencies
from pypi2nix.package import PackageMetadata
from pypi2nix.package import PyprojectToml
from pypi2nix.package import SetupCfg
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.requirements import VersionRequirement
from pypi2nix.target_platform import TargetPlatform


class SourceDistribution(HasBuildDependencies):
    def __init__(
        self,
        name: str,
        logger: Logger,
        requirement_parser: RequirementParser,
        pyproject_toml: Optional[PyprojectToml] = None,
        setup_cfg: Optional[SetupCfg] = None,
    ) -> None:
        self.name = canonicalize_name(name)
        self.pyproject_toml = pyproject_toml
        self.setup_cfg = setup_cfg
        self.logger = logger
        self.requirement_parser = requirement_parser

    @property
    def package_format(self) -> str:
        if self.pyproject_toml:
            return "pyproject"
        else:
            return "setuptools"

    @classmethod
    def from_archive(
        source_distribution,
        archive: Archive,
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> "SourceDistribution":
        with archive.extracted_files() as extraction_directory:
            first_level_paths = os.listdir(extraction_directory)
            if len(first_level_paths) != 1:
                raise DistributionNotDetected(
                    f"Multiple package directories or files extracted from {archive}"
                )
            package_dir = os.path.join(extraction_directory, first_level_paths[0])
            if not os.path.isdir(package_dir):
                raise DistributionNotDetected(
                    f"No package directory could be extracted from source distribution {archive}"
                )
            extracted_files = [
                os.path.join(package_dir, file_name)
                for file_name in os.listdir(package_dir)
                if os.path.isfile(os.path.join(package_dir, file_name))
            ]
            setup_cfg = source_distribution.get_setup_cfg(
                extracted_files, logger, requirement_parser
            )
            metadata = source_distribution._get_package_metadata(package_dir)
            name = source_distribution._get_name(setup_cfg, metadata, archive)
            pyproject_toml = source_distribution.get_pyproject_toml(
                name, extracted_files, logger, requirement_parser
            )
        return source_distribution(
            name=name,
            pyproject_toml=pyproject_toml,
            setup_cfg=setup_cfg,
            logger=logger,
            requirement_parser=requirement_parser,
        )

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
    def get_setup_cfg(
        _,
        extracted_files: Iterable[str],
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> Optional[SetupCfg]:
        setup_cfg_candidates = [
            filepath
            for filepath in extracted_files
            if os.path.basename(filepath) == "setup.cfg"
        ]
        if setup_cfg_candidates:
            return SetupCfg(
                setup_cfg_path=setup_cfg_candidates[0],
                logger=logger,
                requirement_parser=requirement_parser,
            )
        else:
            return None

    @classmethod
    def _get_package_metadata(self, path: str) -> Optional[PackageMetadata]:
        try:
            return PackageMetadata.from_package_directory(path=path)
        except DistributionNotDetected:
            return None

    @classmethod
    def _get_name(
        self,
        setup_cfg: Optional[SetupCfg],
        metadata: Optional[PackageMetadata],
        archive: Archive,
    ) -> str:
        if setup_cfg and metadata:
            if setup_cfg.name != metadata.name and setup_cfg.name is not None:
                raise DistributionNotDetected(
                    f"Conflicting name information from setup.cfg ({setup_cfg.name}) and PKG-INFO ({metadata.name}) in {archive}"
                )
            else:
                return metadata.name
        elif setup_cfg and setup_cfg.name is not None:
            return setup_cfg.name
        elif metadata is not None:
            return metadata.name
        else:
            raise DistributionNotDetected(
                f"Neither PKG-INFO nor setup.cfg are present in {archive}"
            )

    def to_loose_requirement(self) -> Requirement:
        return VersionRequirement(
            name=self.name,
            versions=[],
            extras=set(),
            environment_markers=None,
            logger=self.logger,
        )

    def build_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        build_dependencies = RequirementSet(target_platform)
        if self.pyproject_toml is not None:
            build_dependencies += self.pyproject_toml.build_dependencies(
                target_platform
            )
        if self.setup_cfg is not None:
            build_dependencies += self.setup_cfg.build_dependencies(target_platform)
        return build_dependencies.filter(
            lambda requirement: requirement.name != self.name
        )

    def __str__(self) -> str:
        return f"SourceDistribution<name={self.name}>"

    def __repr__(self) -> str:
        return f"SourceDistribution(name={self.name}, logger={self.logger}, requirement_parser={self.requirement_parser}, pyproject_toml={self.pyproject_toml}, setup_cfg={self.setup_cfg})"
