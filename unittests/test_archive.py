import os
import os.path

import pytest

from pypi2nix.archive import Archive


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
