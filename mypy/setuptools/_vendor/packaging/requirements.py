from typing import Set

from setuptools._vendor.packaging.markers import Marker


class Requirement:
    def __init__(self, requirement_string: str):
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def extras(self) -> Set[str]:
        ...

    @property
    def marker(self) -> Marker:
        ...
