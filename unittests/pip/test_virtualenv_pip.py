import os.path
import venv

import pytest

from pypi2nix.logger import Logger
from pypi2nix.pip.exceptions import PipFailed
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform


@pytest.fixture
def pip_without_index(
    logger: Logger,
    current_platform: TargetPlatform,
    project_dir: str,
    wheel_distribution_archive_path: str,
    requirement_parser: RequirementParser,
) -> VirtualenvPip:
    pip = VirtualenvPip(
        logger=logger,
        target_platform=current_platform,
        target_directory=os.path.join(project_dir, "pip-without-index-venv"),
        env_builder=venv.EnvBuilder(with_pip=True),
        no_index=True,
        wheel_distribution_path=wheel_distribution_archive_path,
        requirement_parser=requirement_parser,
    )
    pip.prepare_virtualenv()
    return pip


@pytest.fixture
def pip_from_data_directory(
    logger: Logger,
    current_platform: TargetPlatform,
    project_dir: str,
    wheel_distribution_archive_path: str,
    data_directory: str,
    requirement_parser: RequirementParser,
) -> VirtualenvPip:
    pip = VirtualenvPip(
        logger=logger,
        target_platform=current_platform,
        target_directory=os.path.join(project_dir, "pip-without-index-venv"),
        env_builder=venv.EnvBuilder(with_pip=True),
        no_index=True,
        wheel_distribution_path=wheel_distribution_archive_path,
        find_links=[data_directory],
        requirement_parser=requirement_parser,
    )
    pip.prepare_virtualenv()
    return pip


def test_pip_without_index_cannot_download_six(
    pip_without_index: VirtualenvPip,
    download_dir: str,
    requirement_parser: RequirementParser,
    current_platform: TargetPlatform,
) -> None:
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    with pytest.raises(PipFailed):
        pip_without_index.download_sources(requirements, download_dir)


def test_pip_without_index_cannot_be_prepared_without_wheel_supplied(
    logger: Logger,
    current_platform: TargetPlatform,
    project_dir: str,
    requirement_parser: RequirementParser,
) -> None:
    pip = VirtualenvPip(
        logger=logger,
        target_platform=current_platform,
        target_directory=os.path.join(project_dir, "pip-without-index-venv"),
        env_builder=venv.EnvBuilder(with_pip=True),
        no_index=True,
        requirement_parser=requirement_parser,
    )
    with pytest.raises(PipFailed):
        pip.prepare_virtualenv()


def test_pip_with_data_directory_index_can_download_six(
    pip_from_data_directory: VirtualenvPip,
    download_dir: str,
    requirement_parser: RequirementParser,
    current_platform: TargetPlatform,
) -> None:
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip_from_data_directory.download_sources(requirements, download_dir)
