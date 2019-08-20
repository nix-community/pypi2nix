from pypi2nix.utils import prefetch_url

from .switches import nix


@nix
def test_prefetch_url_returns_correct_hash(logger):
    url = "https://github.com/nix-community/pypi2nix/archive/4e85fe7505dd7e703aacc18d9ef45f7e47947a6a.zip"
    expected_hash = "1x3dzqlnryplmxm3z1lnl40y0i2g8n6iynlngq2kkknxj9knjyhv"
    assert prefetch_url(url, logger) == expected_hash
