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
