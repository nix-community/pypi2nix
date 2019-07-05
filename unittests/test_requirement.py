import os

import pytest

from pypi2nix.package_source import GitSource
from pypi2nix.requirements import ParsingFailed
from pypi2nix.requirements import Requirement


def test_requirement_cannot_be_constructed_from_line_containing_newline():
    with pytest.raises(ParsingFailed):
        Requirement.from_line("pypi2nix\n")


def test_requirement_finds_name_of_pypi_packages():
    requirement = Requirement.from_line("pypi2nix")
    assert requirement.name == "pypi2nix"


def test_rqeuirement_detects_source_of_pypi_package_as_none():
    requirement = Requirement.from_line("pypi2nix")
    assert requirement.source is None


def test_requirement_finds_name_of_git_package():
    requirement = Requirement.from_line(
        "git+https://github.com/garbas/pypi2nix.git#egg=pypi2nix"
    )
    assert requirement.name == "pypi2nix"


def test_requirement_finds_name_of_hg_package():
    requirement = Requirement.from_line("hg+https://url.test/repo#egg=testegg")
    assert requirement.name == "testegg"


def test_requirement_finds_name_of_url_package():
    requirement = Requirement.from_line("https://url.test/repo#egg=testegg")
    assert requirement.name == "testegg"


def test_requirement_can_handle_environment_marker():
    requirement = Requirement.from_line("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.name == "pypi2nix"


def test_applies_to_system_works_properly_with_positiv_marker():
    requirement = Requirement.from_line("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.applies_to_system()


def test_applies_to_system_works_properly_with_negative_marker():
    requirement = Requirement.from_line("pypi2nix; os_name != '%s'" % os.name)
    assert not requirement.applies_to_system()


def test_names_of_requirements_are_canonicalized():
    requirement = Requirement.from_line("PyPi2Nix")
    assert requirement.name == "pypi2nix"


def test_to_line_reproduces_canonicalized_name():
    name = "pypi2nix"
    requirement = Requirement.from_line(name)
    assert name in requirement.to_line()


def test_to_line_reproduces_version_specifier():
    line = "pypi2nix < 2.0, >= 1.9"
    requirement = Requirement.from_line(line)
    assert "< 2.0" in requirement.to_line()
    assert ">= 1.9" in requirement.to_line()


def test_from_line_recognizes_git_sources():
    line = "git+https://test.test/test#egg=test-egg"
    requirement = Requirement.from_line(line)
    assert requirement.name == "test-egg"
    assert isinstance(requirement.source, GitSource)


def test_from_line_accepts_requirement_with_marker_including_in_operator():
    requirement = Requirement.from_line("zipfile36; python_version in '3.3 3.4 3.5'")
    assert requirement.name == "zipfile36"


def test_that_applies_to_system_works_with_in_keyword(python_version):
    requirement = Requirement.from_line(
        "pypi2nix; python_version in '{}'".format(python_version)
    )
    assert requirement.applies_to_system()
