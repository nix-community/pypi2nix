from abc import ABCMeta
from abc import abstractmethod
from typing import List

from pypi2nix.requirement_set import RequirementSet


class Pip(metaclass=ABCMeta):
    @abstractmethod
    def download_sources(
        self, requirements: RequirementSet, target_directory: str
    ) -> None:
        pass

    @abstractmethod
    def build_wheels(
        self,
        requirements: RequirementSet,
        target_directory: str,
        source_directories: List[str],
    ) -> None:
        pass

    @abstractmethod
    def install(
        self,
        requirements: RequirementSet,
        source_directories: List[str],
        target_directory: str,
    ) -> None:
        pass

    @abstractmethod
    def freeze(self, python_path: List[str]) -> str:
        pass
