import os

import pytest
from pypi2nix.requirements import ParsingFailed
from pypi2nix.requirements import Requirement


def test_requirement_cannot_be_constructed_from_line_containing_newline():
    with pytest.raises(ParsingFailed):
        Requirement("pypi2nix\n")


def test_requirement_finds_name_of_pypi_packages():
    requirement = Requirement("pypi2nix")
    requirement.parse()
    assert requirement.name == "pypi2nix"


def test_rqeuirement_detects_source_of_pypi_package_as_none():
    requirement = Requirement("pypi2nix")
    assert requirement.source is None


def test_requirement_finds_name_of_git_package():
    requirement = Requirement("git+https://github.com/garbas/pypi2nix.git#egg=pypi2nix")
    assert requirement.name == "pypi2nix"


def test_requirement_finds_name_of_hg_package():
    requirement = Requirement("hg+https://url.test/repo#egg=testegg")
    assert requirement.name == "testegg"


def test_requirement_finds_name_of_url_package():
    requirement = Requirement("https://url.test/repo#egg=testegg")
    assert requirement.name == "testegg"


def test_requirement_can_handle_environment_marker():
    requirement = Requirement("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.name == "pypi2nix"


def test_applies_to_system_works_properly_with_positiv_marker():
    requirement = Requirement("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.applies_to_system()


def test_applies_to_system_works_properly_with_negative_marker():
    requirement = Requirement("pypi2nix; os_name != '%s'" % os.name)
    assert not requirement.applies_to_system()
