import os.path

import pytest

from pypi2nix.requirements_collector import RequirementsCollector


@pytest.fixture
def collector(current_platform):
    return RequirementsCollector(current_platform)


def test_that_we_can_generate_an_empty_requirement_set_from_freshly_constructed_collector(
    current_platform
):
    collector = RequirementsCollector(current_platform)
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
    assert os.path.isabs(requirement.url)
