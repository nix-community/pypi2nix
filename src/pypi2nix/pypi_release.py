from enum import Enum
from enum import unique
from typing import Optional

from attr import attrib
from attr import attrs


@unique
class ReleaseType(Enum):
    UNKNOWN = 0
    SOURCE = 1
    WHEEL = 2
    EGG = 3
    WIN_INSTALLER = 4
    RPM = 5
    MSI = 6


_release_type_mapping = {
    "sdist": ReleaseType.SOURCE,
    "bdist_wheel": ReleaseType.WHEEL,
    "bdist_egg": ReleaseType.EGG,
    "bdist_wininst": ReleaseType.WIN_INSTALLER,
    "bdist_rpm": ReleaseType.RPM,
    "bdist_msi": ReleaseType.MSI,
}


def get_release_type_by_packagetype(packagetype: str) -> Optional[ReleaseType]:
    return _release_type_mapping.get(packagetype)


@attrs(frozen=True)
class PypiRelease:
    url: str = attrib()
    sha256_digest: str = attrib()
    version: str = attrib()
    type: ReleaseType = attrib()
    filename: str = attrib()
