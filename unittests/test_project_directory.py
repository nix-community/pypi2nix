import os.path
import tempfile

import pytest

from pypi2nix.project_directory import PersistentProjectDirectory
from pypi2nix.project_directory import TemporaryProjectDirectory


@pytest.fixture(params=("tempfile", "persistent"))
def project_directory(request,):
    if request.param == "tempfile":
        yield TemporaryProjectDirectory()
    elif request.param == "persistent":
        with TemporaryProjectDirectory() as directory:
            yield PersistentProjectDirectory(path=directory)


def test_can_write_to_project_directory(project_directory):
    with project_directory as directory:
        file_path = os.path.join(directory, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")


def test_tempfile_project_directory_is_deleted_after_exception():
    with pytest.raises(Exception), TemporaryProjectDirectory() as directory:
        path = directory
        raise Exception()
    assert not os.path.exists(path)


def test_persistent_project_directory_is_not_deleted_on_exception():
    with tempfile.TemporaryDirectory() as directory:
        with pytest.raises(Exception), PersistentProjectDirectory(
            path=directory
        ) as _project_dir:
            project_directory = _project_dir
            raise Exception()
        assert os.path.exists(project_directory)
