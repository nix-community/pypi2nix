from typing import Set

from pypi2nix.requirements import Requirement

from .external_dependency import ExternalDependency


class RequirementDependencyRetriever:
    def get_external_dependency_for_requirement(
        self, requirement: Requirement
    ) -> Set[ExternalDependency]:
        return set()
