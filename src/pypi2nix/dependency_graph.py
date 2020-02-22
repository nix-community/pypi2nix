from collections import defaultdict
from typing import DefaultDict
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
        return dependency.name() in self._dependencies[dependent.name()]
