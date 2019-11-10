"""Regression test for https://github.com/nix-community/pypi2nix/issues/363"""
from pypi2nix.requirement_parser import RequirementParser


def test_can_parse_enum_requirement_from_issue_363(
    requirement_parser: RequirementParser
):
    requirement = requirement_parser.parse(
        "enum34 (>=1.0.4) ; (python_version=='2.7' or python_version=='2.6' or python_version=='3.3')"
    )
    assert requirement.name() == "enum34"


def test_can_parse_pyinotify_requirement_from_issue_363(
    requirement_parser: RequirementParser
):
    requirement = requirement_parser.parse(
        "pyinotify (>=0.9.6) ; (sys_platform!='win32' and sys_platform!='darwin' and sys_platform!='sunos5')"
    )
    assert requirement.name() == "pyinotify"
