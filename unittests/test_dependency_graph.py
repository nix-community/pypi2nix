from copy import copy

import pytest

from pypi2nix.dependency_graph import CyclicDependencyOccured
from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Logger
from pypi2nix.requirements import Requirement
from pypi2nix.requirements import VersionRequirement


def test_can_set_runtime_dependencies(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph
):
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    assert dependency_graph.is_runtime_dependency(
        dependent=package_a, dependency=package_b
    )


def test_can_detect_indirect_runtime_dependencies(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
) -> None:
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    dependency_graph.set_runtime_dependency(dependent=package_b, dependency=package_c)
    assert dependency_graph.is_runtime_dependency(
        dependent=package_a, dependency=package_c
    )


def test_cyclic_runtime_dependencies_not_allowed(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph
):
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    with pytest.raises(CyclicDependencyOccured):
        dependency_graph.set_runtime_dependency(
            dependent=package_b, dependency=package_a
        )


def test_can_retriev_all_runtime_dependency_names(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
) -> None:
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    dependency_graph.set_runtime_dependency(dependent=package_b, dependency=package_c)
    assert dependency_graph.get_all_runtime_dependency_names(package_a) == {
        package_a.name(),
        package_b.name(),
        package_c.name(),
    }


def test_can_set_buildtime_dependency(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph
):
    dependency_graph.set_buildtime_dependency(dependent=package_a, dependency=package_b)
    assert dependency_graph.is_buildtime_dependency(
        dependent=package_a, dependency=package_b
    )


def test_build_time_dependencies_dont_show_up_as_runtime_dependencies(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
):
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    dependency_graph.set_buildtime_dependency(dependent=package_b, dependency=package_c)
    assert not dependency_graph.is_runtime_dependency(
        dependent=package_a, dependency=package_c
    )


def test_cannot_add_circular_buildtime_dependencies(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph,
):
    dependency_graph.set_buildtime_dependency(dependent=package_a, dependency=package_b)
    with pytest.raises(CyclicDependencyOccured):
        dependency_graph.set_buildtime_dependency(
            dependent=package_b, dependency=package_a
        )


def test_cannot_add_circular_builtime_dependency_to_runtime_dependency(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph,
):
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    with pytest.raises(CyclicDependencyOccured):
        dependency_graph.set_buildtime_dependency(
            dependent=package_b, dependency=package_a
        )


def test_cannot_add_circular_runtime_dependency_to_buildtime_dependency(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph,
):
    dependency_graph.set_buildtime_dependency(dependent=package_a, dependency=package_b)
    with pytest.raises(CyclicDependencyOccured):
        dependency_graph.set_runtime_dependency(
            dependent=package_b, dependency=package_a
        )


def test_can_add_two_dependencies_graphs_and_runtime_dependencies_are_also_added(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
):
    other_dependency_graph = copy(dependency_graph)
    dependency_graph.set_runtime_dependency(dependent=package_a, dependency=package_b)
    other_dependency_graph.set_runtime_dependency(
        dependent=package_b, dependency=package_c
    )
    sum_graph = dependency_graph + other_dependency_graph
    assert not dependency_graph.is_runtime_dependency(
        dependent=package_a, dependency=package_c
    )
    assert not other_dependency_graph.is_runtime_dependency(
        dependent=package_a, dependency=package_c
    )
    assert sum_graph.is_runtime_dependency(dependent=package_a, dependency=package_c)


def test_can_add_two_dependencies_graphs_and_buildtime_dependencies_are_also_added(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
):
    other_dependency_graph = copy(dependency_graph)
    dependency_graph.set_buildtime_dependency(dependent=package_a, dependency=package_b)
    other_dependency_graph.set_buildtime_dependency(
        dependent=package_b, dependency=package_c
    )
    sum_graph = dependency_graph + other_dependency_graph
    assert not dependency_graph.is_buildtime_dependency(
        dependent=package_a, dependency=package_c
    )
    assert not other_dependency_graph.is_buildtime_dependency(
        dependent=package_a, dependency=package_c
    )
    assert sum_graph.is_buildtime_dependency(dependent=package_a, dependency=package_c)


@pytest.fixture
def package_a(logger: Logger) -> Requirement:
    return VersionRequirement(
        name="package-a",
        versions=[],
        extras=set(),
        environment_markers=None,
        logger=logger,
    )


@pytest.fixture
def package_b(logger: Logger) -> Requirement:
    return VersionRequirement(
        name="package-b",
        versions=[],
        extras=set(),
        environment_markers=None,
        logger=logger,
    )


@pytest.fixture
def package_c(logger: Logger) -> Requirement:
    return VersionRequirement(
        name="package-c",
        versions=[],
        extras=set(),
        environment_markers=None,
        logger=logger,
    )


@pytest.fixture
def dependency_graph() -> DependencyGraph:
    return DependencyGraph()
