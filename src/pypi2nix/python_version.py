from enum import Enum
from enum import unique
from typing import Dict
from typing import List
from typing import Optional


@unique
class PythonVersion(Enum):
    python35 = "python35"
    python36 = "python36"
    python37 = "python37"
    python38 = "python38"
    python3 = "python3"

    def nixpkgs_attribute(self) -> str:
        return self.value  # type: ignore

    def derivation_name(self) -> str:
        return self.value  # type: ignore

    def major_version(self) -> str:
        return self.derivation_name().replace("python", "")[0]


_PYTHON_VERSIONS: Dict[str, PythonVersion] = {
    "3.5": PythonVersion.python35,
    "3.6": PythonVersion.python36,
    "3.7": PythonVersion.python37,
    "3.8": PythonVersion.python38,
}


def python_version_from_version_string(version_string: str) -> Optional[PythonVersion]:
    return _PYTHON_VERSIONS.get(version_string)


available_python_versions: List[str] = [version.name for version in PythonVersion]
