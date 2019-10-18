import os
import os.path
from contextlib import contextmanager

import pytest

from pypi2nix.logger import Logger
from pypi2nix.package_source import PathSource
from pypi2nix.requirements_collector import RequirementsCollector


@contextmanager
def current_working_directory(dir: str):
    current = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(current)


@pytest.fixture
def collector(current_platform, requirement_parser, logger: Logger, project_dir: str):
    return RequirementsCollector(
        current_platform, requirement_parser, logger, project_dir
    )


def test_that_we_can_generate_an_empty_requirement_set_from_freshly_constructed_collector(
    current_platform, requirement_parser, logger: Logger, project_dir: str
):
    collector = RequirementsCollector(
        current_platform, requirement_parser, logger, project_dir
    )
    requirements = collector.requirements()
    assert len(requirements) == 0


def test_that_we_can_add_command_line_requirements_by_name(collector):
    collector.add_line("pytest")
    requirements = collector.requirements()
    assert "pytest" in requirements


def test_that_we_can_add_a_requirements_file_path(collector, tmpdir):
    requirements_txt = tmpdir.join("requirements.txt")
    requirements_lines = ["pytest", "flake8"]
    with open(requirements_txt, "w") as f:
        for requirement in requirements_lines:
            print(requirement, file=f)
    collector.add_file(str(requirements_txt))
    assert "pytest" in collector.requirements()
    assert "flake8" in collector.requirements()


def test_that_requirements_with_relative_paths_are_absolute_paths_after_adding(
    collector
):
    collector.add_line("./path/to/egg#egg=testegg")
    requirement = collector.requirements().get("testegg")
    assert os.path.isabs(requirement.path())


def test_that_sources_can_be_extracted_from_a_collector(collector):
    collector.add_line("path/to/egg#egg=testegg")
    assert "testegg" in collector.sources()


def test_that_relative_paths_are_preserved_in_sources(collector):
    collector.add_line("path/to/egg#egg=testegg")
    testegg_source = collector.sources()["testegg"]
    assert isinstance(testegg_source, PathSource)
    assert testegg_source.path == "path/to/egg"


def test_that_path_paths_from_requirement_files_are_preserved_in_sources(
    collector, tmpdir
):
    with current_working_directory(str(tmpdir)):
        requirements_file_path = tmpdir.join("requirements.txt")
        with open(requirements_file_path, "w") as f:
            print("path/to/egg#egg=testegg", file=f)
        collector.add_file(str(requirements_file_path))
        testegg_source = collector.sources()["testegg"]
        assert isinstance(testegg_source, PathSource)
        assert testegg_source.path == "path/to/egg"


def test_that_path_sources_from_requirement_files_are_preserved_in_sources_relative_to_file(
    collector, tmpdir
):
    with current_working_directory(str(tmpdir)):
        requirements_directory = tmpdir.join("directory")
        requirements_directory.mkdir()
        requirements_file_path = requirements_directory.join("requirements.txt")
        with open(requirements_file_path, "w") as f:
            print("path/to/egg#egg=testegg", file=f)
        collector.add_file(str(requirements_file_path))
        testegg_source = collector.sources()["testegg"]
        assert isinstance(testegg_source, PathSource)
        assert testegg_source.path == "directory/path/to/egg"
