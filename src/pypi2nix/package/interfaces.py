from abc import ABCMeta
from abc import abstractmethod

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform


class HasBuildDependencies(metaclass=ABCMeta):
    @abstractmethod
    def build_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        pass


class HasRuntimeDependencies(metaclass=ABCMeta):
    @abstractmethod
    def runtime_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        pass


class HasPackageName(metaclass=ABCMeta):
    @abstractmethod
    def package_name(self) -> str:
        pass
