from copy import copy
from typing import Set

from pypi2nix.external_dependencies import ExternalDependency
from pypi2nix.requirement_set import RequirementSet

from .lookup import RequirementDependencyRetriever


class ExternalDependencyCollector:
    def __init__(
        self, requirement_dependency_retriever: RequirementDependencyRetriever
    ) -> None:
        self._external_dependencies: Set[ExternalDependency] = set()
        self._requirement_dependency_retriever = requirement_dependency_retriever

    def collect_explicit(self, attribute_name: str) -> None:
        self._external_dependencies.add(ExternalDependency(attribute_name))

    def collect_from_requirements(self, requirements: RequirementSet) -> None:
        for requirement in requirements:
            self._external_dependencies.update(
                self._requirement_dependency_retriever.get_external_dependency_for_requirement(
                    requirement
                )
            )

    def get_collected(self) -> Set[ExternalDependency]:
        return copy(self._external_dependencies)
