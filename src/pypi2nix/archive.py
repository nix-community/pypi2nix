import tarfile
import tempfile
import zipfile
from contextlib import contextmanager
from typing import Iterator


class UnpackingFailed(Exception):
    pass


class Archive:
    def __init__(self, path: str) -> None:
        self.path = path

    @contextmanager
    def extracted_files(self) -> Iterator[str]:
        with tempfile.TemporaryDirectory() as directory:
            self.unpack_archive(directory)
            yield directory

    def unpack_archive(self, target_directory: str) -> None:
        if self.path.endswith(".tar.gz"):
            with tarfile.open(self.path, "r:gz") as tar:
                tar.extractall(path=target_directory)
        elif self.path.endswith(".zip") or self.path.endswith(".whl"):
            with zipfile.ZipFile(self.path) as archive:
                archive.extractall(path=target_directory)
        elif self.path.endswith(".tar.bz2"):
            with tarfile.open(self.path, "r:bz2") as tar:
                tar.extractall(path=target_directory)
        else:
            raise UnpackingFailed(
                "Could not detect archive format for file {}".format(self.path)
            )

    def __str__(self) -> str:
        return f"Archive<path={self.path}>"
