import os
import os.path
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from venv import EnvBuilder

from pypi2nix.logger import Logger
from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.pip import PipFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import cmd


class VirtualenvPip(Pip):
    def __init__(
        self,
        logger: Logger,
        target_platform: TargetPlatform,
        target_directory: str,
        env_builder: EnvBuilder,
        requirement_parser: RequirementParser,
        no_index: bool = False,
        wheel_distribution_path: Optional[str] = None,
        find_links: List[str] = [],
    ) -> None:
        self.logger = logger
        self.target_platform = target_platform
        self.target_directory = target_directory
        self.env_builder = env_builder
        self.no_index = no_index
        self.wheel_distribution_path = wheel_distribution_path
        self.find_links = find_links
        self.requirement_parser = requirement_parser

    def prepare_virtualenv(self) -> None:
        self.env_builder.create(self.target_directory)
        self._execute_pip_command(
            ["install", self._wheel_requirement_name()] + self._maybe_index()
        )

    def download_sources(
        self, requirements: RequirementSet, target_directory: Path
    ) -> None:
        with self._requirements_file(requirements) as requirement_file:
            self._execute_pip_command(
                [
                    "download",
                    "-r",
                    requirement_file,
                    "--dest",
                    str(target_directory),
                    "--no-binary",
                    ":all:",
                ]
                + self._maybe_index()
            )

    def build_wheels(
        self,
        requirements: RequirementSet,
        target_directory: Path,
        source_directories: List[Path],
    ) -> None:
        with self._requirements_file(requirements) as requirement_file:
            source_dir_arguments: List[str] = []
            for source_directory in source_directories:
                source_dir_arguments.append("--find-links")
                source_dir_arguments.append(str(source_directory))
            self._execute_pip_command(
                ["wheel", "--wheel-dir", str(target_directory), "--no-index"]
                + source_dir_arguments
                + ["--requirement", requirement_file]
            )

    def install(
        self,
        requirements: RequirementSet,
        source_directories: List[Path],
        target_directory: Path,
    ) -> None:
        with self._requirements_file(requirements) as requirements_file:
            source_directories_arguments = []
            for source_directory in source_directories:
                source_directories_arguments.append("--find-links")
                source_directories_arguments.append(str(source_directory))
            self._execute_pip_command(
                [
                    "install",
                    "--no-index",
                    "--target",
                    str(target_directory),
                    "-r",
                    requirements_file,
                ]
                + source_directories_arguments
            )

    def freeze(self, python_path: List[Path]) -> str:
        return self._execute_pip_command(["freeze"], pythonpath=python_path)

    def _pip_path(self) -> str:
        return os.path.join(self.target_directory, "bin", "pip")

    def _execute_pip_command(
        self, arguments: List[str], pythonpath: List[Path] = []
    ) -> str:
        with self._explicit_pythonpath(pythonpath), self._set_environment_variable(
            {"SOURCE_DATE_EPOCH": "315532800",}
        ):
            returncode, output = cmd([self._pip_path()] + arguments, logger=self.logger)
        if returncode != 0:
            raise PipFailed(output=output)
        return output

    @contextmanager
    def _explicit_pythonpath(self, pythonpath: List[Path]) -> Iterator[None]:
        additional_paths = ":".join(map(str, pythonpath))
        with self._set_environment_variable({"PYTHONPATH": additional_paths}):
            yield

    @contextmanager
    def _requirements_file(self, requirements: RequirementSet) -> Iterator[str]:
        with TemporaryDirectory() as directory:
            yield requirements.to_file(
                directory, self.target_platform, self.requirement_parser, self.logger
            ).processed_requirements_file_path()

    @contextmanager
    def _set_environment_variable(
        self, variables: Dict[str, Optional[str]]
    ) -> Iterator[None]:
        def set_environment(environment: Dict[str, Optional[str]]) -> None:
            for name, value in variables.items():
                if value is None:
                    del os.environ[name]
                else:
                    os.environ[name] = value

        old_environment = dict(os.environ)
        set_environment(variables)
        try:
            yield
        finally:
            for key, value in old_environment.items():
                os.environ[key] = value
            for key in os.environ.keys():
                if key not in old_environment:
                    del os.environ[key]

    def _maybe_index(self) -> List[str]:
        arguments: List[str] = []
        if self.no_index:
            arguments.append("--no-index")
        for link in self.find_links:
            arguments.append("--find-links")
            arguments.append(link)
        return arguments

    def _wheel_requirement_name(self) -> str:
        if self.wheel_distribution_path is None:
            return "wheel"
        else:
            return self.wheel_distribution_path
