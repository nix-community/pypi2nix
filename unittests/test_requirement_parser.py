from pypi2nix.requirements import requirement_parser


def test_parses_pip_style_url():
    requirement_parser.compiled_grammar()(
        "git+https://github.com/garbas/pypi2nix.git"
    ).URI_pip_style()


def test_parse_pip_style_requirement():
    requirement_parser.compiled_grammar()(
        "git+https://github.com/garbas/pypi2nix.git#egg=pypi2nix"
    ).url_req_pip_style()


def test_environment_marker_works_properly_with_in(python_version):
    marker = requirement_parser.compiled_grammar()("python_version in '1 2 3'").marker()
    assert marker == ("in", python_version, "1 2 3")


def test_environment_marker_is_propagated_properly(python_version):
    name, extras, version, marker = requirement_parser.compiled_grammar()(
        "zipfile36; python_version in '3.3 3.4 3.5'"
    ).specification()
    assert name == "zipfile36"
    assert extras == []
    assert version == []
    assert marker == ("in", python_version, "3.3 3.4 3.5")


def test_that_python_implemntation_marker_can_be_parsed():
    requirement_parser.compiled_grammar()(
        'testspec; python_implementation == "CPython"'
    )
