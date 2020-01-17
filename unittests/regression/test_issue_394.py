# https://github.com/nix-community/pypi2nix/issues/394
from pypi2nix.requirement_parser import RequirementParser


def test_can_parse_requirements_with_comments(requirement_parser: RequirementParser):
    requirement = requirement_parser.parse("requirement # comment")
    assert requirement.name() == "requirement"


def test_can_parse_given_test_case_from_issue(requirement_parser: RequirementParser):
    requirement = requirement_parser.parse("aioredis  # my favourite package")
    assert requirement.name() == "aioredis"
