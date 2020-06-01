from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.external_dependencies import ExternalDependency
from pypi2nix.external_dependency_collector import RequirementDependencyRetriever
from pypi2nix.requirement_parser import RequirementParser


def test_no_external_dependency_for_empty_dependency_graph(
    requirement_parser: RequirementParser,
) -> None:
    dependency_graph = DependencyGraph()
    retriever = RequirementDependencyRetriever(dependency_graph)
    requirement = requirement_parser.parse("testpackage")
    assert not retriever.get_external_dependency_for_requirement(requirement)


def test_external_dependencies_from_graph_are_retrieved(
    requirement_parser: RequirementParser,
) -> None:
    dependency_graph = DependencyGraph()
    requirement = requirement_parser.parse("testpackage")
    external_dependency = ExternalDependency("external")
    dependency_graph.set_external_dependency(
        dependent=requirement, dependency=external_dependency
    )
    retriever = RequirementDependencyRetriever(dependency_graph)
    assert external_dependency in retriever.get_external_dependency_for_requirement(
        requirement
    )
