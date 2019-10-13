import pytest

from pypi2nix.nix import Nix
from pypi2nix.package_source import GitSource
from pypi2nix.package_source import HgSource
from pypi2nix.package_source import PathSource
from pypi2nix.package_source import UrlSource

from .switches import nix

URL_SOURCE_URL = "https://github.com/nix-community/pypi2nix/archive/4e85fe7505dd7e703aacc18d9ef45f7e47947a6a.zip"
URL_SOURCE_HASH = "1x3dzqlnryplmxm3z1lnl40y0i2g8n6iynlngq2kkknxj9knjyhv"


@pytest.fixture
def git_source():
    return GitSource(
        url="https://github.com/nix-community/pypi2nix.git",
        revision="4e85fe7505dd7e703aacc18d9ef45f7e47947a6a",
    )


@pytest.fixture
def hg_source(logger):
    return HgSource(
        url="https://bitbucket.org/tarek/flake8", revision="a209fb69350c", logger=logger
    )


@pytest.fixture
def url_source(logger):
    return UrlSource(url=URL_SOURCE_URL, logger=logger)


@pytest.fixture
def path_source():
    return PathSource("/test/path")


@pytest.fixture
def expression_evaluater(logger):
    nix_instance = Nix(logger=logger)
    return lambda expression: nix_instance.evaluate_expression(
        "let pkgs = import <nixpkgs> {}; in " + expression
    )


@nix
def test_git_source_gives_correct_hash_value(git_source):
    assert (
        git_source.hash_value()
        == "113sngkfi93pdlws1i8kq2rqff10xr1n3z3krn2ilq0fdrddyk96"
    )


@nix
def test_git_source_produces_valid_nix_expression(git_source, expression_evaluater):
    expression_evaluater(git_source.nix_expression())


@nix
def test_hg_source_gives_correct_hash_value(hg_source):
    assert (
        hg_source.hash_value() == "1n0fzlzmfmynnay0n757yh3qwjd9xxcfi7vq4sxqvsv90c441s7v"
    )


@nix
def test_hg_source_produces_valid_nix_expression(hg_source, expression_evaluater):
    expression_evaluater(hg_source.nix_expression())


@nix
def test_url_source_gives_correct_hash_value(url_source):
    assert url_source.hash_value() == URL_SOURCE_HASH


@nix
def test_url_source_gives_valid_nix_expression(url_source, expression_evaluater):
    expression_evaluater(url_source.nix_expression())


def test_url_source_nix_expression_contains_specified_hash_when_given(logger):
    # We specify the wrong hash on purpose to see that UrlSource just
    # "accepts" the given hash and puts it into the generated nix
    # expression
    url_source = UrlSource(
        URL_SOURCE_URL, hash_value=URL_SOURCE_HASH + "1", logger=logger
    )
    assert URL_SOURCE_HASH + "1" in url_source.nix_expression()


@nix
def test_path_source_gives_valid_nix_expression(path_source, expression_evaluater):
    expression_evaluater(path_source.nix_expression())


def test_path_source_paths_with_one_segement_get_dot_appended_for_nix():
    source = PathSource("segment")
    assert source.nix_expression() == "segment/."
