from collections import defaultdict
from typing import DefaultDict
from typing import Generator
from typing import Set

from pypi2nix.requirements import Requirement


class DependencyGraph:
    def __init__(self) -> None:
        self._runtime_dependencies: DefaultDict[str, Set[str]] = defaultdict(
            lambda: set()
        )
        self._buildtime_dependencies: DefaultDict[str, Set[str]] = defaultdict(
            lambda: set()
        )

    def set_runtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        if self.is_buildtime_dependency(dependency, dependent):
            raise CyclicDependencyOccured(
                f"Failed to add dependency {dependent} -> {dependency} to Graph "
                f"since {dependent} is alread a dependency of {dependency}"
            )
        self._runtime_dependencies[dependent.name()].add(dependency.name())

    def set_buildtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        if self.is_buildtime_dependency(dependency, dependent):
            raise CyclicDependencyOccured(
                f"Failed to add dependency {dependent} -> {dependency} to Graph "
                f"since {dependent} is alread a dependency of {dependency}"
            )
        self._buildtime_dependencies[dependent.name()].add(dependency.name())

    def is_runtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> bool:
        return self._is_runtime_child(dependent.name(), dependency.name())

    def is_buildtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> bool:
        return self._is_python_child(dependent.name(), dependency.name())

    def get_all_runtime_dependency_names(self, package: Requirement) -> Set[str]:
        return set(self._get_runtime_children(package.name()))

    def _is_python_child(self, dependent: str, dependency: str) -> bool:
        for child in self._get_python_children(dependent):
            if child == dependency:
                return True
        return False

    def _is_runtime_child(self, dependent: str, dependency: str) -> bool:
        for child in self._get_runtime_children(dependent):
            if child == dependency:
                return True
        return False

    def _get_python_children(self, package_name: str) -> Generator[str, None, None]:
        alread_seen: Set[str] = set()
        pending: Set[str] = {package_name}
        while pending:
            package = pending.pop()
            yield package
            alread_seen.add(package)
            for dependency in (
                self._runtime_dependencies[package]
                | self._buildtime_dependencies[package]
            ):
                if dependency in alread_seen:
                    continue
                else:
                    pending.add(dependency)

    def _get_runtime_children(self, package_name: str) -> Generator[str, None, None]:
        alread_seen: Set[str] = set()
        pending: Set[str] = {package_name}
        while pending:
            package = pending.pop()
            yield package
            alread_seen.add(package)
            for dependency in self._runtime_dependencies[package]:
                if dependency in alread_seen:
                    continue
                else:
                    pending.add(dependency)


class CyclicDependencyOccured(Exception):
    pass
