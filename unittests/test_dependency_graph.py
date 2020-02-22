import pytest

from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Logger
from pypi2nix.requirements import Requirement
from pypi2nix.requirements import VersionRequirement


def test_can_set_direct_dependencies(
    package_a: Requirement, package_b: Requirement, dependency_graph: DependencyGraph
):
    dependency_graph.set_direct_dependency(dependent=package_a, dependency=package_b)
    assert dependency_graph.is_dependency(dependent=package_a, dependency=package_b)


def test_can_detect_indirect_dependencies(
    package_a: Requirement,
    package_b: Requirement,
    package_c: Requirement,
    dependency_graph: DependencyGraph,
) -> None:
    dependency_graph.set_direct_dependency(dependent=package_a, dependency=package_b)
    dependency_graph.set_direct_dependency(dependent=package_b, dependency=package_c)
    assert dependency_graph.is_dependency(dependent=package_a, dependency=package_c)


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
