import os

import pytest
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.source_distribution import SourceDistribution

from .switches import nix


@pytest.fixture
def source_distribution(six_source_distribution):
    return SourceDistribution.from_tarball(six_source_distribution)


@pytest.fixture
def flit_distribution(pip, project_dir, download_dir):
    requirements = [RequirementsFile.from_lines(["flit"], project_dir)]
    pip.download_sources(requirements, download_dir)
    distributions = [
        SourceDistribution.from_tarball(os.path.join(download_dir, filename))
        for filename in os.listdir(download_dir)
    ]
    for distribution in distributions:
        if distribution.name == "flit":
            return distribution


@nix
def test_from_tarball_picks_up_on_name(source_distribution):
    assert source_distribution.name == "six"


@nix
def test_six_package_has_no_pyproject_toml(source_distribution):
    assert source_distribution.pyproject_toml is None


@nix
def test_that_flit_pyproject_toml_is_recognized(flit_distribution):
    assert flit_distribution.pyproject_toml is not None
