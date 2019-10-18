import pytest
from parsley import ParseError

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements import PathRequirement

from .logger import get_logger_output


def test_parses_pip_style_url(requirement_parser):
    requirement_parser.compiled_grammar()(
        "git+https://github.com/nix-community/pypi2nix.git"
    ).URI_pip_style()


def test_parse_pip_style_requirement(requirement_parser):
    requirement_parser.compiled_grammar()(
        "git+https://github.com/nix-community/pypi2nix.git#egg=pypi2nix"
    ).url_req_pip_style()


def test_that_python_implemntation_marker_can_be_parsed(requirement_parser):
    requirement_parser.compiled_grammar()(
        'testspec; python_implementation == "CPython"'
    )


@pytest.mark.parametrize("path", ("/test/path", "./test/path", "test/path", "./."))
def test_that_file_path_with_leading_slash_can_be_parsed(path, requirement_parser):
    assert requirement_parser.compiled_grammar()(path).file_path() == path


@pytest.mark.parametrize(
    "path", ("#", "/#/", "/test#/", "#/test", "path/test#egg=testegg")
)
def test_that_path_with_hashpound_is_not_recognized(path, requirement_parser):
    with pytest.raises(ParseError):
        requirement_parser.compiled_grammar()(path).file_path()


def test_that_we_can_parse_pip_style_requirement_with_file_path(requirement_parser):
    requirement = requirement_parser.compiled_grammar()(
        "path/to/egg#egg=testegg"
    ).path_req_pip_style()
    assert requirement.name() == "testegg"
    assert requirement.path() == "path/to/egg"


@pytest.mark.parametrize(
    "line",
    (
        "cffi>=1.8,!=1.11.3; python_implementation != 'PyPy'",
        "cffi>=1.1; python_implementation != 'PyPy'",
        "cffi>=1.4.1; python_implementation != 'PyPy'",
    ),
)
def test_regressions_with_cryptography(
    requirement_parser: RequirementParser, line: str, logger: Logger
) -> None:
    requirement = requirement_parser.parse(line)
    assert requirement.name() == "cffi"
    assert "WARNING" in get_logger_output(logger)
    assert "PEP 508" in get_logger_output(logger)


def test_that_path_is_parsed_to_path_requirement(requirement_parser: RequirementParser):
    requirement = requirement_parser.parse("local_path/egg#egg=local-path")
    assert isinstance(requirement, PathRequirement)


def test_that_requirement_parser_does_not_choke_on_sys_dot_platform(
    requirement_parser: RequirementParser, logger: Logger
):
    line = 'macfsevents ; sys.platform == "darwin"'
    requirement = requirement_parser.parse(line)
    assert requirement.name() == "macfsevents"
    assert "WARNING" in get_logger_output(logger)
    assert "PEP 508" in get_logger_output(logger)
