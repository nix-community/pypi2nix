from typing import List
from typing import Optional

from attr import attrib
from attr import attrs

from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.logger import Verbosity
from pypi2nix.overrides import Overrides
from pypi2nix.path import Path
from pypi2nix.python_version import PythonVersion


@attrs
class ApplicationConfiguration:
    verbosity: Verbosity = attrib()
    nix_executable_directory: Optional[str] = attrib()
    nix_path: List[str] = attrib()
    extra_build_inputs: List[str] = attrib()
    emit_extra_build_inputs: bool = attrib()
    extra_environment: str = attrib()
    enable_tests: bool = attrib()
    python_version: PythonVersion = attrib()
    requirement_files: List[str] = attrib()
    requirements: List[str] = attrib()
    setup_requirements: List[str] = attrib()
    overrides: List[Overrides] = attrib()
    wheels_caches: List[str] = attrib()
    output_basename: str = attrib()
    project_directory: Path = attrib()
    target_directory: str = attrib()
    dependency_graph_output_location: Optional[Path] = attrib()
    dependency_graph_input: DependencyGraph = attrib()
