from typing import Dict

PYTHON_VERSIONS: Dict[str, str] = {
    "2.6": "python26Full",
    "2.7": "python27Full",
    "3.2": "python32",
    "3.3": "python33",
    "3.4": "python34",
    "3.5": "python35",
    "3.6": "python36",
    "3.7": "python37",
    "3": "python3",
    "pypy": "pypy",
}


available_python_versions = list(PYTHON_VERSIONS.keys())
