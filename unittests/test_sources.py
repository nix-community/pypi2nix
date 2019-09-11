import pytest

from pypi2nix.package_source import PathSource
from pypi2nix.sources import Sources


@pytest.fixture
def sources():
    return Sources()


@pytest.fixture
def other_sources():
    return Sources()


def test_sources_can_be_added_to(sources):
    sources.add("testsource", PathSource("/test/path"))

    assert "testsource" in sources


def test_sources_can_be_queried_by_name(sources):
    source = PathSource("/test/path")
    sources.add("testsource", source)

    assert sources["testsource"] is source


def test_sources_can_be_merged(sources, other_sources):
    assert "testsource" not in sources
    other_sources.add("testsource", PathSource("/test/path"))
    sources.update(other_sources)
    assert "testsource" in sources


def test_items_returns_length_on_tuple_for_one_entry(sources):
    sources.add("testitem", PathSource("/test/path"))
    assert len(sources.items()) == 1


def test_empty_sources_has_length_0(sources):
    assert len(sources) == 0
