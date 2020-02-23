from io import StringIO

from hypothesis import given
from hypothesis.strategies import booleans
from hypothesis.strategies import composite
from hypothesis.strategies import integers
from hypothesis.strategies import lists
from hypothesis.strategies import text

from pypi2nix.dependency_graph import CyclicDependencyOccured
from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.external_dependencies import ExternalDependency
from pypi2nix.logger import StreamLogger
from pypi2nix.requirements import VersionRequirement

logger = StreamLogger(output=StringIO())


@composite
def requirement(draw, name=text(min_size=1)):
    return VersionRequirement(
        name=draw(name),
        logger=logger,
        versions=[],
        extras=set(),
        environment_markers=None,
    )


@composite
def external_dependency(draw, attribute_name=text(min_size=1)):
    return ExternalDependency(attribute_name=draw(attribute_name))


@composite
def dependency_graph(
    draw,
    python_packages=lists(requirement(), unique_by=lambda x: x.name()),
    external_dependencies=lists(external_dependency()),
    is_runtime_dependency=booleans(),
    selections=integers(),
):
    graph = DependencyGraph()
    packages = draw(python_packages)
    if not packages:
        return graph
    for package in packages:
        index = draw(selections) % len(packages)
        try:
            if draw(is_runtime_dependency):
                graph.set_runtime_dependency(
                    dependent=package, dependency=packages[index]
                )
            else:
                graph.set_buildtime_dependency(
                    dependent=package, dependency=packages[index]
                )
        except CyclicDependencyOccured:
            continue
    for dependency in draw(external_dependencies):
        graph.set_external_dependency(
            dependent=packages[draw(selections) % len(packages)],
            dependency=dependency
        )
    return graph


@given(dependency_graph=dependency_graph())
def test_equality_to_self(dependency_graph):
    assert dependency_graph == dependency_graph


def test_equality_of_empty_graphs():
    assert DependencyGraph() == DependencyGraph()


@given(dependency_graph=dependency_graph())
def test_serialization_and_deserialization_leads_to_identity(
    dependency_graph: DependencyGraph,
):
    assert DependencyGraph.deserialize(dependency_graph.serialize()) == dependency_graph
