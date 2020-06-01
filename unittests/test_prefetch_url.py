import pytest

from pypi2nix.utils import prefetch_url

from .switches import nix


@nix
def test_prefetch_url_returns_correct_hash(logger):
    url = "https://github.com/nix-community/pypi2nix/archive/4e85fe7505dd7e703aacc18d9ef45f7e47947a6a.zip"
    expected_hash = "1x3dzqlnryplmxm3z1lnl40y0i2g8n6iynlngq2kkknxj9knjyhv"
    assert prefetch_url(url, logger) == expected_hash


@nix
def test_prefetch_url_raises_on_invalid_name(logger):
    """nix-prefetch-url cannot handle file names with period in them. Here
    we test if the code throws a ValueError in that instance.
    """
    url = "https://raw.githubusercontent.com/nix-community/pypi2nix/6fe6265b62b53377b4677a39c6ee48550c1f2186/.gitignore"
    with pytest.raises(ValueError):
        prefetch_url(url, logger)


@nix
def test_can_provide_name_so_prefetch_does_not_fail(logger):
    url = "https://raw.githubusercontent.com/nix-community/pypi2nix/6fe6265b62b53377b4677a39c6ee48550c1f2186/.gitignore"
    sha256 = prefetch_url(url, logger, name="testname")
    assert sha256 == "0b2s1lyfr12v83rrb69j1cfcsksisgwyzfl5mix6qz5ldxfww8p0"
