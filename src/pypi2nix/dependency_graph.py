from collections import defaultdict
from copy import copy
from typing import Callable
from typing import DefaultDict
from typing import Dict
from typing import Generator
from typing import List
from typing import Set
from typing import TypeVar

import yaml

from pypi2nix.external_dependencies import ExternalDependency
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements import Requirement
from pypi2nix.wheel import Wheel

K = TypeVar("K")
V = TypeVar("V")


class DependencyGraph:
    def __init__(self) -> None:
        self._runtime_dependencies: DefaultDict[str, Set[str]] = defaultdict(
            lambda: set()
        )
        self._buildtime_dependencies: DefaultDict[str, Set[str]] = defaultdict(
            lambda: set()
        )
        self._external_dependencies: DefaultDict[
            str, Set[ExternalDependency]
        ] = defaultdict(lambda: set())

    def set_runtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        self._raise_on_cyclic_dependency(dependent, dependency)
        self._runtime_dependencies[dependent.name()].add(dependency.name())

    def set_buildtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        self._raise_on_cyclic_dependency(dependent, dependency)
        self._buildtime_dependencies[dependent.name()].add(dependency.name())

    def set_external_dependency(
        self, dependent: Requirement, dependency: ExternalDependency
    ) -> None:
        self._external_dependencies[dependent.name()].add(dependency)

    def is_runtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> bool:
        return self._is_runtime_child(dependent.name(), dependency.name())

    def is_buildtime_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> bool:
        return self._is_python_child(dependent.name(), dependency.name())

    def get_all_build_dependency_names(self, package: Requirement) -> Set[str]:
        return set(self._get_python_children(package.name()))

    def get_all_runtime_dependency_names(self, package: Requirement) -> Set[str]:
        return set(self._get_runtime_children(package.name()))

    def get_all_external_dependencies(
        self, package: Requirement
    ) -> Set[ExternalDependency]:
        found_dependencies: Set[ExternalDependency] = set()
        for package_name in self._get_python_children(package.name()):
            found_dependencies.update(self._external_dependencies[package_name])
        return found_dependencies

    def import_wheel(self, wheel: Wheel, requirement_parser: RequirementParser) -> None:
        dependent = requirement_parser.parse(wheel.name)
        for runtime_dependency in wheel.runtime_dependencies(wheel.target_platform()):

            self.set_runtime_dependency(dependent, runtime_dependency)
        for build_dependency in wheel.build_dependencies(wheel.target_platform()):
            self.set_buildtime_dependency(dependent, build_dependency)

    def serialize(self) -> str:
        document: DefaultDict[str, Dict[str, List[str]]] = defaultdict(lambda: dict())
        for key, external_dependencies in self._external_dependencies.items():
            document[key]["externalDependencies"] = [
                dep.attribute_name() for dep in external_dependencies
            ]
        for key, runtime_dependencies in self._runtime_dependencies.items():
            document[key]["runtimeDependencies"] = list(runtime_dependencies)
        for key, buildtime_dependencies in self._buildtime_dependencies.items():
            document[key]["buildtimeDependencies"] = list(buildtime_dependencies)
        return yaml.dump(dict(document))  # type: ignore

    @classmethod
    def deserialize(_class, data: str) -> "DependencyGraph":
        document: DefaultDict[str, Dict[str, List[str]]]
        document = yaml.load(data, Loader=yaml.Loader)
        graph = DependencyGraph()
        for package, dependencies in document.items():
            external_dependencies = dependencies.get("externalDependencies")
            if external_dependencies is not None:
                graph._external_dependencies[package] = {
                    ExternalDependency(name) for name in external_dependencies
                }
            runtime_dependencies = dependencies.get("runtimeDependencies")
            if runtime_dependencies is not None:
                graph._runtime_dependencies[package] = set(runtime_dependencies)
            buildtime_dependencies = dependencies.get("buildtimeDependencies")
            if buildtime_dependencies is not None:
                graph._buildtime_dependencies[package] = set(buildtime_dependencies)
        return graph

    def _raise_on_cyclic_dependency(
        self, dependent: Requirement, dependency: Requirement
    ) -> None:
        if self.is_buildtime_dependency(dependency, dependent):
            raise CyclicDependencyOccured(
                f"Failed to add dependency {dependent} -> {dependency} to Graph "
                f"since {dependent} is alread a dependency of {dependency}"
            )

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

    def __add__(self, other: "DependencyGraph") -> "DependencyGraph":
        new_graph = DependencyGraph()
        new_graph._runtime_dependencies = _merge_defaultdicts(
            self._runtime_dependencies, other._runtime_dependencies
        )
        new_graph._buildtime_dependencies = _merge_defaultdicts(
            self._buildtime_dependencies, other._buildtime_dependencies
        )
        new_graph._external_dependencies = _merge_defaultdicts(
            self._external_dependencies, other._external_dependencies
        )
        return new_graph

    def __copy__(self) -> "DependencyGraph":
        new_graph = DependencyGraph()
        new_graph._buildtime_dependencies = copy(self._buildtime_dependencies)
        new_graph._runtime_dependencies = copy(self._runtime_dependencies)
        new_graph._external_dependencies = copy(self._external_dependencies)
        return new_graph

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DependencyGraph):
            return (
                self._runtime_dependencies == other._runtime_dependencies
                and self._buildtime_dependencies == other._buildtime_dependencies
                and self._external_dependencies == other._external_dependencies
            )
        else:
            return False

    def __repr__(self) -> str:
        return (
            "DependencyGraph("
            f"runtime_dependencies={repr(self._runtime_dependencies)}, "
            f"buildtime_dependencies={repr(self._buildtime_dependencies)}, "
            f"external_dependencies={repr(self._external_dependencies)}"
            ")"
        )


class CyclicDependencyOccured(Exception):
    pass


def _merge_defaultdicts(
    first: DefaultDict[str, Set[V]], second: DefaultDict[str, Set[V]]
) -> DefaultDict[str, Set[V]]:
    return _merge_with_combine(
        first, second, combine_function=lambda x, y: x | y, constructor=lambda: set(),
    )


def _merge_with_combine(
    first: DefaultDict[K, V],
    second: DefaultDict[K, V],
    combine_function: Callable[[V, V], V],
    constructor: Callable[[], V],
) -> DefaultDict[K, V]:
    combination: DefaultDict[K, V] = defaultdict(constructor)
    for first_key, first_value in first.items():
        combination[first_key] = first_value
    for second_key, second_value in second.items():
        combination[second_key] = (
            combine_function(combination[second_key], second_value)
            if second_key in combination
            else second_value
        )
    return combination
