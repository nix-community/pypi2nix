import os.path
from typing import Dict
from typing import List
from typing import Optional

from pypi2nix.logger import Logger
from pypi2nix.utils import NixOption
from pypi2nix.utils import cmd
from pypi2nix.utils import create_command_options


class ExecutableNotFound(FileNotFoundError):
    pass


class EvaluationFailed(Exception):
    def __init__(self, *args, output: Optional[str] = None, **kwargs):  # type: ignore
        super().__init__(self, *args, **kwargs)  # type: ignore
        self.output: Optional[str] = output


class Nix:
    def __init__(
        self,
        logger: Logger,
        nix_path: List[str] = [],
        executable_directory: Optional[str] = None,
    ):
        self.nix_path = nix_path
        self.executable_directory = executable_directory
        self.logger = logger

    def evaluate_expression(self, expression: str) -> str:
        output = self.run_nix_command(
            "nix-instantiate", ["--eval", "--expr", expression]
        )
        # cut off the last newline character append to the output
        return output[:-1]

    def shell(
        self,
        command: str,
        derivation_path: str,
        nix_arguments: Dict[str, NixOption] = {},
        pure: bool = True,
    ) -> str:
        output = self.run_nix_command(
            "nix-shell",
            create_command_options(nix_arguments)
            + (["--pure"] if pure else [])
            + [derivation_path, "--command", command],
        )
        return output

    def build(
        self,
        source_file: str,
        attribute: Optional[str] = None,
        out_link: Optional[str] = None,
        arguments: Dict[str, NixOption] = dict(),
    ) -> None:
        self.run_nix_command(
            "nix-build",
            [source_file]
            + (["-o", out_link] if out_link else [])
            + (["-A", attribute] if attribute else [])
            + create_command_options(arguments),
        )

    def build_expression(
        self,
        expression: str,
        out_link: Optional[str] = None,
        arguments: Dict[str, NixOption] = dict(),
    ) -> None:
        self.run_nix_command(
            "nix-build",
            ["--expr", expression]
            + (["-o", out_link] if out_link else [])
            + create_command_options(arguments),
        )

    def run_nix_command(self, binary_name: str, command: List[str]) -> str:
        final_command = (
            [self.executable_path(binary_name)] + self.nix_path_arguments() + command
        )
        returncode: int
        output: str
        try:
            returncode, output = cmd(final_command, self.logger)
        except FileNotFoundError:
            raise ExecutableNotFound(
                "Could not find executable '{program}'".format(program=binary_name)
            )
        if returncode != 0:
            raise EvaluationFailed(
                "'{program}' exited with non-zero exit code ({code}).".format(
                    program=binary_name, code=returncode
                ),
                output=output,
            )
        return output

    def nix_path_arguments(self) -> List[str]:
        path_arguments = []
        for path in self.nix_path:
            path_arguments.append("-I")
            path_arguments.append(path)
        return path_arguments

    def executable_path(self, program_name: str) -> str:
        if self.executable_directory is None:
            return program_name
        else:
            return os.path.join(self.executable_directory, program_name)
