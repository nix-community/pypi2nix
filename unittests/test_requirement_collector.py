import os
import os.path
import pathlib
from contextlib import contextmanager
from typing import Any
from typing import Generator

import pytest

from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Logger
from pypi2nix.package_source import PathSource
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements import PathRequirement
from pypi2nix.requirements_collector import RequirementsCollector
from pypi2nix.target_platform import TargetPlatform


@contextmanager
def current_working_directory(dir: str) -> Generator[None, None, None]:
    current = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(current)


@pytest.fixture
def collector(
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    project_dir: str,
) -> RequirementsCollector:
    return RequirementsCollector(
        current_platform, requirement_parser, logger, project_dir, DependencyGraph()
    )


def test_that_we_can_generate_an_empty_requirement_set_from_freshly_constructed_collector(
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    project_dir: str,
) -> None:
    collector = RequirementsCollector(
        current_platform, requirement_parser, logger, project_dir, DependencyGraph()
    )
    requirements = collector.requirements()
    assert len(requirements) == 0


def test_that_we_can_add_command_line_requirements_by_name(
    collector: RequirementsCollector,
) -> None:
    collector.add_line("pytest")
    requirements = collector.requirements()
    assert "pytest" in requirements


def test_that_we_can_add_a_requirements_file_path(
    collector: RequirementsCollector, tmpdir: pathlib.Path
) -> None:
    requirements_txt = tmpdir / "requirements.txt"
    requirements_lines = ["pytest", "flake8"]
    with open(requirements_txt, "w") as f:
        for requirement in requirements_lines:
            print(requirement, file=f)
    collector.add_file(str(requirements_txt))
    assert "pytest" in collector.requirements()
    assert "flake8" in collector.requirements()


def test_that_requirements_with_relative_paths_are_absolute_paths_after_adding(
    collector: RequirementsCollector,
) -> None:
    collector.add_line("./path/to/egg#egg=testegg")
    requirement = collector.requirements().get("testegg")
    assert isinstance(requirement, PathRequirement)
    assert os.path.isabs(requirement.path())


def test_that_sources_can_be_extracted_from_a_collector(
    collector: RequirementsCollector,
) -> None:
    collector.add_line("path/to/egg#egg=testegg")
    assert "testegg" in collector.sources()


def test_that_relative_paths_are_preserved_in_sources(
    collector: RequirementsCollector,
) -> None:
    collector.add_line("path/to/egg#egg=testegg")
    testegg_source = collector.sources()["testegg"]
    assert isinstance(testegg_source, PathSource)
    assert testegg_source.path == "path/to/egg"


def test_that_path_paths_from_requirement_files_are_preserved_in_sources(
    collector: RequirementsCollector, tmpdir: Any
) -> None:
    with current_working_directory(str(tmpdir)):
        requirements_file_path = tmpdir.join("requirements.txt")
        with open(requirements_file_path, "w") as f:
            print("path/to/egg#egg=testegg", file=f)
        collector.add_file(str(requirements_file_path))
        testegg_source = collector.sources()["testegg"]
        assert isinstance(testegg_source, PathSource)
        assert testegg_source.path == "path/to/egg"


def test_that_path_sources_from_requirement_files_are_preserved_in_sources_relative_to_file(
    collector: RequirementsCollector, tmpdir: Any
) -> None:
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
