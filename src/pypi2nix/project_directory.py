import tempfile
from abc import ABCMeta
from abc import abstractmethod
from sys import stderr
from types import TracebackType
from typing import Optional
from typing import Type


class ProjectDirectory(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> str:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type],
        exc_value: Optional[Exception],
        traceback: Optional[TracebackType],
    ) -> None:
        pass


class TemporaryProjectDirectory(ProjectDirectory):
    def __init__(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()

    def __enter__(self) -> str:
        return self.temporary_directory.__enter__()

    def __exit__(
        self,
        exc_type: Optional[Type],
        exc_value: Optional[Exception],
        traceback: Optional[TracebackType],
    ) -> None:
        return self.temporary_directory.__exit__(exc_type, exc_value, traceback)


class PersistentProjectDirectory(ProjectDirectory):
    def __init__(self, path: str) -> None:
        self.path = path

    def __enter__(self) -> str:
        print(
            "WARNING: You have specified the `--build-directory OPTION`.", file=stderr
        )
        print("WARNING: It is recommended to not use this flag.", file=stderr)
        return self.path

    def __exit__(
        self,
        exc_type: Optional[Type],
        exc_value: Optional[Exception],
        traceback: Optional[TracebackType],
    ) -> None:
        pass
