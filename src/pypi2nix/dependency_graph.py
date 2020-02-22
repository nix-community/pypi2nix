from collections import defaultdict
from typing import DefaultDict
from typing import Generator
from typing import Set

from pypi2nix.requirements import Requirement


class DependencyGraph:
    def __init__(self) -> None:
        self._dependencies: DefaultDict[str, Set[str]] = defaultdict(lambda: set())

    def set_direct_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        self._dependencies[dependent.name()].add(dependency.name())

    def is_dependency(self, dependent: Requirement, dependency: Requirement) -> bool:
        return self._is_child(dependent.name(), dependency.name())

    def get_dependency_names(self, package: Requirement) -> Set[str]:
        return set(self._get_children(package.name()))

    def _is_child(self, dependent: str, dependency: str) -> bool:
        for child in self._get_children(dependent):
            if child == dependency:
                return True
        return False

    def _get_children(self, package_name: str) -> Generator[str, None, None]:
        alread_seen: Set[str] = set()
        pending: Set[str] = {package_name}
        while pending:
            package = pending.pop()
            yield package
            alread_seen.add(package)
            for dependency in self._dependencies[package]:
                if dependency in alread_seen:
                    continue
                else:
                    pending.add(dependency)
