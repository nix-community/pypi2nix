import os

import pytest

from pypi2nix.package_source import GitSource
from pypi2nix.requirements import IncompatibleRequirements
from pypi2nix.requirements import ParsingFailed
from pypi2nix.requirements import PathRequirement
from pypi2nix.requirements import Requirement
from pypi2nix.requirements import UrlRequirement

from .switches import nix


def test_requirement_cannot_be_constructed_from_line_containing_newline():
    with pytest.raises(ParsingFailed):
        Requirement.from_line("pypi2nix\n >= 1.0")


def test_requirement_finds_name_of_pypi_packages():
    requirement = Requirement.from_line("pypi2nix")
    assert requirement.name() == "pypi2nix"


def test_requirement_detects_source_of_pypi_package_as_none():
    requirement = Requirement.from_line("pypi2nix")
    assert requirement.source() is None


def test_requirement_finds_name_of_git_package():
    requirement = Requirement.from_line(
        "git+https://github.com/garbas/pypi2nix.git#egg=pypi2nix"
    )
    assert requirement.name() == "pypi2nix"


def test_requirement_finds_name_of_hg_package():
    requirement = Requirement.from_line("hg+https://url.test/repo#egg=testegg")
    assert requirement.name() == "testegg"


def test_requirement_finds_name_of_url_package():
    requirement = Requirement.from_line("https://url.test/repo#egg=testegg")
    assert requirement.name() == "testegg"


def test_requirement_can_handle_environment_marker():
    requirement = Requirement.from_line("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.name() == "pypi2nix"


def test_applies_to_target_works_properly_with_positiv_marker(current_platform):
    requirement = Requirement.from_line("pypi2nix; os_name == '%s'" % os.name)
    assert requirement.applies_to_target(current_platform)


def test_applies_to_target_works_properly_with_negative_marker(current_platform):
    requirement = Requirement.from_line("pypi2nix; os_name != '%s'" % os.name)
    assert not requirement.applies_to_target(current_platform)


@pytest.mark.parametrize(
    "line, expected",
    [
        ("PyPi2Nix", "pypi2nix"),
        ("TestReq >= 1.0", "testreq"),
        ("path/to/req#egg=test_req", "test-req"),
        ("https://test.test#egg=Test_Req", "test-req"),
    ],
)
def test_names_of_requirements_are_canonicalized(line, expected):
    requirement = Requirement.from_line(line)
    assert requirement.name() == expected


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
    assert requirement.name() == "test-egg"
    assert isinstance(requirement.source(), GitSource)


def test_from_line_accepts_requirement_with_marker_including_in_operator():
    requirement = Requirement.from_line("zipfile36; python_version in '3.3 3.4 3.5'")
    assert requirement.name() == "zipfile36"


def test_that_applies_to_target_works_with_in_keyword(current_platform):
    requirement = Requirement.from_line(
        "pypi2nix; python_version in '{}'".format(current_platform.version)
    )
    assert requirement.applies_to_target(current_platform)


def test_that_mercurial_source_url_gets_detected():
    requirement = Requirement.from_line(
        "hg+https://bitbucket.org/tarek/flake8@a209fb6#egg=flake8"
    )
    assert requirement.url() == "hg+https://bitbucket.org/tarek/flake8@a209fb6"


@nix
def test_that_mercurial_source_extracted_is_valid():
    requirement = Requirement.from_line(
        "hg+https://bitbucket.org/tarek/flake8@a209fb6#egg=flake8"
    )
    # We only want this to not throw
    requirement.source().nix_expression()


@nix
def test_that_git_source_extracted_is_valid():
    requirement = Requirement.from_line(
        "git+https://github.com/nix-community/pypi2nix.git@5c65345a2ce7f2f1c376f983d20e935c09c15995#egg=pypi2nix"
    )
    # We only want this to not throw
    requirement.source().nix_expression()


def test_that_from_line_to_line_preserves_urls():
    line = "git+https://example.test/#egg=testegg"
    requirement = Requirement.from_line(line)
    assert requirement.to_line() == line


def test_that_requirements_can_be_added_together_adding_version_constraints(
    current_platform
):
    req1 = Requirement.from_line("req >= 1.0")
    req2 = Requirement.from_line("req >= 2.0")
    sum_requirement = req1.add(req2, current_platform)
    assert len(sum_requirement.version()) == len(req1.version()) + len(req2.version())


def test_that_adding_requirements_with_different_names_throws(current_platform):
    req1 = Requirement.from_line("req1")
    req2 = Requirement.from_line("req2")
    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)


def test_that_adding_requirements_with_a_version_and_a_url_results_in_url_requirement(
    current_platform
):
    for direction in ["forward", "reverse"]:
        req1 = Requirement.from_line("req1 >= 1.0")
        req2 = Requirement.from_line("git+https://test.test/path#egg=req1")
        if direction == "forward":
            sum_requirement = req1.add(req2, current_platform)
        else:
            sum_requirement = req2.add(req1, current_platform)

        assert isinstance(sum_requirement, UrlRequirement)
        assert sum_requirement.url() == "git+https://test.test/path"


def test_that_adding_requirements_with_different_urls_raises(current_platform):
    req1 = Requirement.from_line("https://url1.test#egg=req")
    req2 = Requirement.from_line("https://url2.test#egg=req")
    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)


def test_that_adding_requirements_with_the_same_url_works(current_platform):
    req1 = Requirement.from_line("https://url.test#egg=req")
    req2 = Requirement.from_line("https://url.test#egg=req")
    assert (req1.add(req2, current_platform)).url() == "https://url.test"


def test_that_adding_requirements_where_one_does_not_apply_to_system_yields_the_other(
    current_platform
):
    req1 = Requirement.from_line("req1")
    req2 = Requirement.from_line(
        'req1 >= 1.0; python_version == "1.0"'
    )  # definitly not true
    sum_requirement = req1.add(req2, current_platform)
    assert not sum_requirement.version()


def test_that_we_parse_requirements_with_file_paths():
    requirement = Requirement.from_line("path/to/egg#egg=testegg")
    assert requirement.name() == "testegg"
    assert requirement.path() == "path/to/egg"


@pytest.mark.parametrize(
    "req_line_1",
    ["req", "req <= 1.0", "https://test.test#egg=req", "path/to/egg#egg=req"],
)
@pytest.mark.parametrize("req_line_2", ["req", "req <= 2.0"])
def test_that_we_can_add_two(req_line_1, req_line_2, current_platform):
    requirement1 = Requirement.from_line(req_line_1)
    requirement2 = Requirement.from_line(req_line_2)
    requirement1.add(requirement2, current_platform)


@pytest.mark.parametrize(
    "version_requirement_line",
    (
        "test-req",
        "test-req <= 1.0",
        "test-req; 'python_version' == '3.7'",
        "test-req; 'python_version' != '3.7'",
    ),
)
@pytest.mark.parametrize(
    "path_requirement_line",
    ("path/to/req#egg=test-req", "path/to/req#egg=test-req[extra]"),
)
def test_that_we_can_add_version_with_path_requirement_result_is_path_requirement(
    version_requirement_line, path_requirement_line, current_platform
):
    req1 = Requirement.from_line(version_requirement_line)
    req2 = Requirement.from_line(path_requirement_line)
    sum_requirement = req1.add(req2, current_platform)
    assert isinstance(sum_requirement, PathRequirement)

    sum_requirement = req2.add(req1, current_platform)
    assert isinstance(sum_requirement, PathRequirement)


@pytest.mark.parametrize(
    "version_requirement_line",
    (
        "test-req",
        "test-req <= 1.0",
        "test-req; 'python_version' == '3.7'",
        "test-req; 'python_version' != '3.7'",
    ),
)
@pytest.mark.parametrize(
    "url_requirement_line",
    ("https://test.test/#egg=test-req", "https://test.test/#egg=test-req[extra]"),
)
def test_can_add_version_requirement_with_url_requirement(
    version_requirement_line, url_requirement_line, current_platform
):
    req1 = Requirement.from_line(version_requirement_line)
    req2 = Requirement.from_line(url_requirement_line)
    sum_requirement = req1.add(req2, current_platform)
    assert isinstance(sum_requirement, UrlRequirement)

    sum_requirement = req2.add(req1, current_platform)
    assert isinstance(sum_requirement, UrlRequirement)


@pytest.mark.parametrize(
    "url_requirement_line",
    ("https://test.test#egg=test-req", "https://test.test#egg=test-req[extra1]"),
)
@pytest.mark.parametrize(
    "path_requirement_line",
    ("path/to/req#egg=test-req", "path/to/req#egg=test-req[extra2]"),
)
def test_cannot_add_path_and_url_requirement(
    path_requirement_line, url_requirement_line, current_platform
):
    req1 = Requirement.from_line(path_requirement_line)
    req2 = Requirement.from_line(url_requirement_line)
    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)

    with pytest.raises(IncompatibleRequirements):
        req2.add(req1, current_platform)


def test_cannot_add_requirements_with_different_paths(current_platform):
    req1 = Requirement.from_line("path/1#egg=test-req")
    req2 = Requirement.from_line("path/2#egg=test-req")

    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)


def test_that_we_cannot_add_path_requirements_with_different_names(current_platform):
    req1 = Requirement.from_line("path/to/req#egg=req1")
    req2 = Requirement.from_line("path/to/req#egg=req2")

    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)


def test_adding_path_requirements_where_one_requirement_does_not_apply(
    current_platform
):
    req1 = Requirement.from_line("path/to/req#egg=test-req")
    req2 = Requirement.from_line(
        'different/path#egg=test-req; "python_version" == "1.0"'
    )

    assert req1.add(req2, current_platform) == req1
    assert req2.add(req1, current_platform) == req1


def test_that_we_can_add_path_requirements_with_same_path(current_platform,):
    req1 = Requirement.from_line("path/to/requirement#egg=test-req")
    req2 = Requirement.from_line("path/to/requirement#egg=test-req")

    assert req1.add(req2, current_platform) == req1


def test_that_we_can_change_path_of_path_requirements():
    requirement = Requirement.from_line("path/to/requirement#egg=test-req")
    requirement = requirement.change_path(lambda p: os.path.join("changed", p))
    assert requirement.path() == "changed/path/to/requirement"


def test_that_we_can_add_url_requirements_where_one_does_not_apply(current_platform):
    req1 = Requirement.from_line("https://test.test#egg=test-req")
    req2 = Requirement.from_line(
        'https://other.test#egg=test-req; "python_version" == "1.0"'
    )
    assert req1.add(req2, current_platform) == req1
    assert req2.add(req1, current_platform) == req1


def test_cannot_add_url_requirements_with_different_names(current_platform):
    req1 = Requirement.from_line("https://test.test#egg=req1")
    req2 = Requirement.from_line("https://test.test#egg=req2")
    with pytest.raises(IncompatibleRequirements):
        req1.add(req2, current_platform)
