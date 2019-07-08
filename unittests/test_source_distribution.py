import os

import pytest

from pypi2nix.archive import Archive
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.source_distribution import SourceDistribution

from .switches import nix


@pytest.fixture
def source_distribution(six_source_distribution_archive):
    return SourceDistribution.from_archive(six_source_distribution_archive)


@pytest.fixture
def flit_requirements():
    requirements = RequirementSet()
    requirements.add(Requirement.from_line("flit == 1.3"))
    return requirements


@pytest.fixture
def flit_distribution(pip, project_dir, download_dir, flit_requirements):
    pip.download_sources(flit_requirements, download_dir)
    archives = [
        Archive(path=os.path.join(download_dir, filename))
        for filename in os.listdir(download_dir)
    ]
    distributions = list(map(SourceDistribution.from_archive, archives))
    for distribution in distributions:
        if distribution.name == "flit":
            return distribution


@nix
def test_from_archive_picks_up_on_name(source_distribution):
    assert source_distribution.name == "six"


@nix
def test_that_a_source_distributions_name_is_canonicalized():
    distribution = SourceDistribution(name="NaMe_teSt")
    assert distribution.name == "name-test"


@nix
def test_six_package_has_no_pyproject_toml(source_distribution):
    assert source_distribution.pyproject_toml is None


@nix
def test_that_flit_pyproject_toml_is_recognized(flit_distribution):
    assert flit_distribution.pyproject_toml is not None


@nix
def test_that_flit_build_dependencies_contains_requests(
    flit_distribution, current_platform
):
    assert "requests" in flit_distribution.build_dependencies(current_platform)


@nix
def test_that_we_can_generate_objects_from_source_archives(source_distribution_archive):
    SourceDistribution.from_archive(source_distribution_archive)


@nix
def test_that_we_can_detect_setup_requirements_for_setup_cfg_projects(
    distribution_archive_for_jsonschema, current_platform
):
    distribution = SourceDistribution.from_archive(distribution_archive_for_jsonschema)
    assert "setuptools-scm" in distribution.build_dependencies(current_platform)
