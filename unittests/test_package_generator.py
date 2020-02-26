from pathlib import Path

import pytest

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser

from .package_generator import PackageGenerator


def test_can_gerate_source_distribution_with_correct_name(package_generator):
    distribution = package_generator.generate_setuptools_package(name="testpackage")
    assert distribution.name == "testpackage"


@pytest.fixture
def target_directory(tmpdir):
    return tmpdir


@pytest.fixture
def package_generator(
    logger: Logger, target_directory: Path, requirement_parser: RequirementParser
) -> PackageGenerator:
    return PackageGenerator(
        target_directory=target_directory,
        logger=logger,
        requirement_parser=requirement_parser,
    )
