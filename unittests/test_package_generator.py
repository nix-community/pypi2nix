import venv
from pathlib import Path

import pytest

from pypi2nix.logger import Logger
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from .package_generator import PackageGenerator


def test_can_generate_two_packages(package_generator: PackageGenerator):
    package_generator.generate_setuptools_package(name="package1",)
    package_generator.generate_setuptools_package(name="package2",)


def test_can_gerate_source_distribution_with_correct_name(
    package_generator: PackageGenerator,
):
    distribution = package_generator.generate_setuptools_package(name="testpackage")
    assert distribution.name == "testpackage"


def test_can_install_generated_packages(
    pip,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    target_directory: Path,
    install_target: Path,
    package_generator: PackageGenerator,
):
    package_generator.generate_setuptools_package(name="testpackage")
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("testpackage"))
    pip.install(
        requirements,
        source_directories=[str(target_directory)],
        target_directory=str(install_target),
    )
    assert "testpackage" in pip.freeze(python_path=[str(install_target)])


@pytest.fixture
def pip(
    logger: Logger,
    current_platform: TargetPlatform,
    target_directory: Path,
    wheel_distribution_archive_path: str,
    requirement_parser: RequirementParser,
    install_target: Path,
) -> VirtualenvPip:
    pip = VirtualenvPip(
        logger=logger,
        target_platform=current_platform,
        target_directory=str(install_target),
        env_builder=venv.EnvBuilder(with_pip=True),
        no_index=True,
        wheel_distribution_path=wheel_distribution_archive_path,
        find_links=[str(target_directory)],
        requirement_parser=requirement_parser,
    )
    pip.prepare_virtualenv()
    return pip


@pytest.fixture
def target_directory(tmpdir_factory):
    return tmpdir_factory.mktemp("target-directory")


@pytest.fixture
def install_target(tmpdir_factory):
    return tmpdir_factory.mktemp("install-target")


@pytest.fixture
def package_generator(
    logger: Logger, target_directory: Path, requirement_parser: RequirementParser
) -> PackageGenerator:
    return PackageGenerator(
        target_directory=target_directory,
        logger=logger,
        requirement_parser=requirement_parser,
    )
