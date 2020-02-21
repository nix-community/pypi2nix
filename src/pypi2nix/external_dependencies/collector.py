from copy import copy
from typing import List

from .external_dependency import ExternalDependency


class ExternalDependencyCollector:
    def __init__(self) -> None:
        self._external_dependencies: List[ExternalDependency] = []

    def collect_explicit(self, attribute_name: str) -> None:
        self._external_dependencies.append(ExternalDependency(attribute_name))

    def get_collected(self) -> List[ExternalDependency]:
        return copy(self._external_dependencies)
