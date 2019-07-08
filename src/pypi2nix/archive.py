import tarfile
import tempfile
import zipfile
from contextlib import contextmanager


class UnpackingFailed(Exception):
    pass


class Archive:
    def __init__(self, path):
        self.path = path

    @contextmanager
    def contents(self):
        with tempfile.TemporaryDirectory() as directory:
            self.unpack_archive(directory)
            yield directory

    def unpack_archive(self, target_directory):
        if self.path.endswith(".tar.gz"):
            with tarfile.open(self.path, "r:gz") as tar:
                tar.extractall(path=target_directory)
        elif self.path.endswith(".zip"):
            with zipfile.ZipFile(self.path) as archive:
                archive.extractall(path=target_directory)
        else:
            raise UnpackingFailed(
                "Could not detect archive format for file {}".format(self.path)
            )
