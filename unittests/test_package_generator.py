import venv

import pytest

from pypi2nix.logger import Logger
from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from .package_generator import PackageGenerator


def test_can_generate_two_packages(package_generator: PackageGenerator) -> None:
    package_generator.generate_setuptools_package(name="package1",)
    package_generator.generate_setuptools_package(name="package2",)


def test_can_gerate_source_distribution_with_correct_name(
    package_generator: PackageGenerator,
):
    distribution = package_generator.generate_setuptools_package(name="testpackage")
    assert distribution.name == "testpackage"


def test_can_install_generated_packages(
    pip: Pip,
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
        source_directories=[target_directory],
        target_directory=install_target,
    )
    assert "testpackage" in pip.freeze(python_path=[install_target])


def test_can_generate_packages_with_requirements(
    package_generator: PackageGenerator,
    requirement_parser: RequirementParser,
    pip: Pip,
    target_directory: Path,
    install_target: Path,
    current_platform: TargetPlatform,
):
    package_generator.generate_setuptools_package(
        name="testpackage", install_requires=["other-package"]
    )
    package_generator.generate_setuptools_package(name="other-package")
    requirements = RequirementSet(target_platform=current_platform)
    requirements.add(requirement_parser.parse("testpackage"))
    pip.install(
        requirements,
        source_directories=[target_directory],
        target_directory=install_target,
    )
    assert "other-package" in pip.freeze([install_target])


def test_can_generate_valid_packages_with_two_runtime_dependencies(
    package_generator: PackageGenerator,
    requirement_parser: RequirementParser,
    pip: Pip,
    target_directory: Path,
    install_target: Path,
    current_platform: TargetPlatform,
):
    package_generator.generate_setuptools_package(
        name="testpackage", install_requires=["dependency1", "dependency2"]
    )
    package_generator.generate_setuptools_package(name="dependency1")
    package_generator.generate_setuptools_package(name="dependency2")
    requirements = RequirementSet(target_platform=current_platform)
    requirements.add(requirement_parser.parse("testpackage"))
    pip.install(
        requirements,
        source_directories=[target_directory],
        target_directory=install_target,
    )
    installed_packages = pip.freeze([install_target])
    assert "dependency1" in installed_packages
    assert "dependency2" in installed_packages


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
        env_builder=venv.EnvBuilder(with_pip=True, symlinks=True),
        no_index=True,
        wheel_distribution_path=wheel_distribution_archive_path,
        find_links=[str(target_directory)],
        requirement_parser=requirement_parser,
    )
    pip.prepare_virtualenv()
    return pip


@pytest.fixture
def target_directory(tmpdir_factory) -> Path:
    return Path(str(tmpdir_factory.mktemp("target-directory")))


@pytest.fixture
def install_target(tmpdir_factory) -> Path:
    return Path(str(tmpdir_factory.mktemp("install-target")))


@pytest.fixture
def package_generator(
    logger: Logger, target_directory: Path, requirement_parser: RequirementParser
) -> PackageGenerator:
    return PackageGenerator(
        target_directory=target_directory,
        logger=logger,
        requirement_parser=requirement_parser,
    )
