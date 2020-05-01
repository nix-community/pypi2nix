from typing import Set

from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.external_dependencies import ExternalDependency
from pypi2nix.requirements import Requirement


class RequirementDependencyRetriever:
    def __init__(self, dependency_graph: DependencyGraph = DependencyGraph()):
        self._dependency_graph = dependency_graph

    def get_external_dependency_for_requirement(
        self, requirement: Requirement
    ) -> Set[ExternalDependency]:
        return self._dependency_graph.get_all_external_dependencies(requirement)
