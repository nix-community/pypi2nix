from typing import Set

from attr import attrib
from attr import attrs

from pypi2nix.pypi_release import PypiRelease


@attrs
class PypiPackage:
    name: str = attrib()
    releases: Set[PypiRelease] = attrib()
    version: str = attrib()
