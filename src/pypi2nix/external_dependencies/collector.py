from copy import copy
from typing import List

from pypi2nix.requirement_set import RequirementSet

from .external_dependency import ExternalDependency
from .lookup import RequirementDependencyRetriever


class ExternalDependencyCollector:
    def __init__(
        self, requirement_dependency_retriever: RequirementDependencyRetriever
    ) -> None:
        self._external_dependencies: List[ExternalDependency] = []
        self._requirement_dependency_retriever = requirement_dependency_retriever

    def collect_explicit(self, attribute_name: str) -> None:
        self._external_dependencies.append(ExternalDependency(attribute_name))

    def collect_from_requirements(self, requirements: RequirementSet) -> None:
        for requirement in requirements:
            self._external_dependencies += self._requirement_dependency_retriever.get_external_dependency_for_requirement(
                requirement
            )

    def get_collected(self) -> List[ExternalDependency]:
        return copy(self._external_dependencies)
