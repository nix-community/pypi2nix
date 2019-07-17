import pytest
from parsley import ParseError

from pypi2nix.requirements import requirement_parser


def test_parses_pip_style_url():
    requirement_parser.compiled_grammar()(
        "git+https://github.com/garbas/pypi2nix.git"
    ).URI_pip_style()


def test_parse_pip_style_requirement():
    requirement_parser.compiled_grammar()(
        "git+https://github.com/garbas/pypi2nix.git#egg=pypi2nix"
    ).url_req_pip_style()


def test_that_python_implemntation_marker_can_be_parsed():
    requirement_parser.compiled_grammar()(
        'testspec; python_implementation == "CPython"'
    )


@pytest.mark.parametrize("path", ("/test/path", "./test/path", "test/path", "./."))
def test_that_file_path_with_leading_slash_can_be_parsed(path):
    assert requirement_parser.compiled_grammar()(path).file_path() == path


@pytest.mark.parametrize(
    "path", ("#", "/#/", "/test#/", "#/test", "path/test#egg=testegg")
)
def test_that_path_with_hashpound_is_not_recognized(path):
    with pytest.raises(ParseError):
        requirement_parser.compiled_grammar()(path).file_path()


def test_that_we_can_parse_pip_style_requirement_with_file_path():
    name, extras, path, marker = requirement_parser.compiled_grammar()(
        "path/to/egg#egg=testegg"
    ).url_req_pip_style()
    assert name == "testegg"
    assert path == "path/to/egg"
