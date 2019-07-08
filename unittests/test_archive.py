import os
import os.path

import pytest

from pypi2nix.archive import Archive

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def test_txt_content():
    path = os.path.join(DATA_DIRECTORY, "test.txt")
    with open(path) as f:
        return f.read()


@pytest.fixture
def test_tar_gz_path():
    return os.path.join(DATA_DIRECTORY, "test.tar.gz")


@pytest.fixture
def test_zip_path():
    return os.path.join(DATA_DIRECTORY, "test.zip")


@pytest.fixture(params=("tar", "zip"))
def archive(request, test_zip_path, test_tar_gz_path):
    if request.param == "tar":
        return Archive(path=test_tar_gz_path)
    else:
        return Archive(path=test_zip_path)


def test_that_we_can_inspect_the_content_of_an_archive(archive):
    with archive.contents() as directory:
        files = tuple(os.listdir(directory))
        assert files == ("test.txt",)
