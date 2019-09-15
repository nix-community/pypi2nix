import os
import os.path

import pytest

from pypi2nix.archive import Archive


@pytest.fixture(params=("tar", "zip", "bz2"))
def archive(request, test_zip_path, test_tar_gz_path, test_tar_bz2_path):
    if request.param == "tar":
        return Archive(path=test_tar_gz_path)
    elif request.param == "bz2":
        return Archive(path=test_tar_bz2_path)
    else:
        return Archive(path=test_zip_path)


def test_that_we_can_inspect_the_content_of_an_archive(archive):
    with archive.extracted_files() as directory:
        files = tuple(os.listdir(directory))
        assert files == ("test.txt",)


def test_that_we_can_inspect_the_content_of_a_wheel(setupcfg_package_wheel_path: str):
    archive = Archive(path=setupcfg_package_wheel_path)
    with archive.extracted_files() as directory:
        assert "setupcfg_package-1.0.dist-info" in os.listdir(directory)
