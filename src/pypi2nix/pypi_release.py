from enum import Enum
from enum import unique

from attr import attrib
from attr import attrs


@unique
class ReleaseType(Enum):
    UNKNOWN = 0
    SOURCE = 1
    WHEEL = 2


@attrs(frozen=True)
class PypiRelease:
    url: str = attrib()
    sha256_digest: str = attrib()
    version: str = attrib()
    type: ReleaseType = attrib()
