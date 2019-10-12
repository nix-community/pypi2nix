import os.path
import shlex
import shutil
import sys
import urllib.parse
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import click

from pypi2nix.logger import Logger
from pypi2nix.nix import EvaluationFailed
from pypi2nix.nix import Nix
from pypi2nix.pip.interface import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import escape_double_quotes

HERE = os.path.dirname(__file__)
DOWNLOAD_NIX = os.path.join(HERE, "download.nix")
WHEEL_NIX = os.path.join(HERE, "wheel.nix")
INSTALL_NIX = os.path.join(HERE, "install.nix")
BASE_NIX = os.path.join(HERE, "base.nix")


class NixPip(Pip):
    def __init__(
        self,
        nix: Nix,
        project_directory: str,
        extra_build_inputs: List[str],
        extra_env: str,
        wheels_cache: List[str],
        target_platform: TargetPlatform,
        logger: Logger,
        requirement_parser: RequirementParser,
    ):
        self.nix = nix
        self.project_directory = project_directory
        self.extra_build_inputs = extra_build_inputs
        self.extra_env = extra_env
        self.build_output: str = ""
        self.wheels_cache = wheels_cache
        self.target_platform = target_platform
        self.logger = logger
        self.requirement_parser = requirement_parser

        output = self.nix.evaluate_expression(
            'let pkgs = import <nixpkgs> {}; in "%s"' % escape_double_quotes(extra_env)
        )
        # trim quotes
        self.extra_env = output[1:-1]

        self.default_lib_directory = os.path.join(self.project_directory, "lib")
        self.download_cache_directory = os.path.join(self.project_directory, "cache")

    def download_sources(
        self, requirements: RequirementSet, target_directory: str
    ) -> None:
        if not requirements:
            return
        requirements_files = [
            requirements.to_file(
                self.project_directory,
                self.target_platform,
                self.requirement_parser,
                self.logger,
            ).processed_requirements_file_path()
        ]
        self.build_from_nix_file(
            command="exit",
            file_path=DOWNLOAD_NIX,
            nix_arguments=self.nix_arguments(
                requirements_files=requirements_files,
                destination_directory=target_directory,
                editable_sources_directory=self.editable_sources_directory(),
                build_directory=self.build_directory(),
            ),
        )

    def build_wheels(
        self,
        requirements: RequirementSet,
        target_directory: str,
        source_directories: List[str],
    ) -> None:
        if not requirements:
            return
        requirements_files = [
            requirements.to_file(
                self.project_directory,
                self.target_platform,
                self.requirement_parser,
                self.logger,
            ).processed_requirements_file_path()
        ]
        self.build_from_nix_file(
            command="exit",
            file_path=WHEEL_NIX,
            nix_arguments=self.nix_arguments(
                wheels_cache=self.wheels_cache,
                requirements_files=requirements_files,
                editable_sources_directory=self.editable_sources_directory(),
                build_directory=self.build_directory(),
                wheels_dir=target_directory,
                sources=source_directories,
            ),
        )

    def install(
        self,
        requirements: RequirementSet,
        source_directories: List[str],
        target_directory: Optional[str] = None,
    ) -> None:
        if not requirements:
            return
        if target_directory is None:
            target_directory = self.default_lib_directory
        requirements_files = [
            requirements.to_file(
                self.project_directory,
                self.target_platform,
                self.requirement_parser,
                self.logger,
            ).processed_requirements_file_path()
        ]
        self.build_from_nix_file(
            command="exit",
            file_path=INSTALL_NIX,
            nix_arguments=self.nix_arguments(
                requirements_files=requirements_files,
                target_directory=target_directory,
                sources_directories=source_directories,
            ),
        )

    def freeze(self, python_path: List[str] = []) -> str:
        additional_paths = ":".join(map(shlex.quote, python_path))

        output: str = self.nix.shell(
            "{PYTHONPATH} pip freeze".format(
                PYTHONPATH="PYTHONPATH=" + additional_paths + ':"$PYTHONPATH"'
                if python_path
                else ""
            ),
            BASE_NIX,
            nix_arguments=self.nix_arguments(),
        )
        lines = map(lambda x: x.strip(), output.splitlines())
        return ("\n".join(lines) + "\n") if lines else ""

    def editable_sources_directory(self) -> str:
        return os.path.join(self.project_directory, "editable_sources")

    def build_directory(self) -> str:
        return os.path.join(self.project_directory, "build")

    def nix_arguments(self, **arguments) -> Dict[str, Any]:  # type: ignore
        return dict(
            dict(
                download_cache_dir=self.download_cache_directory,
                extra_build_inputs=self.extra_build_inputs,
                project_dir=self.project_directory,
                python_version=self.target_platform.nixpkgs_python_version.derivation_name(),
                extra_env=self.extra_env,
            ),
            **arguments,
        )

    def build_from_nix_file(
        self, file_path: str, command: str, nix_arguments: Any
    ) -> None:
        self.create_download_cache_if_missing()
        self.delete_build_directory()
        try:
            self.build_output = self.nix.shell(
                command=command, derivation_path=file_path, nix_arguments=nix_arguments
            )
        except EvaluationFailed as error:
            if error.output is not None:
                self.build_output += error.output
            is_failure = True
        else:
            is_failure = False
        self.handle_build_error(is_failure=is_failure)

    def create_download_cache_if_missing(self) -> None:
        if os.path.exists(self.download_cache_directory):
            pass
        else:
            os.makedirs(self.download_cache_directory)

    def delete_build_directory(self) -> None:
        try:
            shutil.rmtree(self.build_directory())
        except FileNotFoundError:
            pass

    def handle_build_error(self, is_failure: bool) -> None:
        if not is_failure:
            if not self.build_output.endswith(
                "ERROR: Failed to build one or more wheels"
            ):
                return

        self.logger.error(self.build_output)

        message = "While trying to run the command something went wrong."

        # trying to recognize the problem and provide more meanigful error
        # message
        no_matching_dist = "No matching distribution found for "
        if no_matching_dist in self.build_output:
            dist_name = self.build_output[
                self.build_output.find(no_matching_dist) + len(no_matching_dist) :
            ]
            dist_name = dist_name[: dist_name.find(" (from")]
            message = (
                "Most likely `%s` package does not have source (zip/tar.bz) "
                "distribution." % dist_name
            )

        else:
            try:
                self.send_crash_report()
            except OSError:
                self.logger.error("Failed to send crash report")

        raise click.ClickException(message)

    def send_crash_report(self) -> None:
        if click.confirm(
            "Do you want to report above issue (a browser "
            "will open with prefilled details of issue)?"
        ):
            title = "Error when running pypi2nix command"
            body = "# Description\n\n<detailed description of error "
            "here>\n\n"
            body += "# Traceback \n\n```bash\n"
            body += "% pypi2nix --version\n"
            with open(os.path.join(HERE, "VERSION")) as f:
                body += f.read() + "\n"
            body += "% pypi2nix " + " ".join(sys.argv[1:]) + "\n"
            body += self.build_output + "\n```\n"
            click.launch(
                "https://github.com/nix-community/pypi2nix/issues/new?%s"
                % (urllib.parse.urlencode(dict(title=title, body=body)))
            )
