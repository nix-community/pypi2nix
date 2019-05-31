import os.path
import subprocess

from pypi2nix.utils import cmd
from pypi2nix.utils import create_command_options


class ExecutableNotFound(FileNotFoundError):
    pass


class EvaluationFailed(Exception):
    def __init__(self, *args, output=None, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.output = output


class Nix:
    def __init__(self, nix_path=[], executable_directory=None, verbose=False):
        self.nix_path = nix_path
        self.executable_directory = executable_directory
        self.verbose = verbose

    def evaluate_expression(self, expression):
        output = self.run_nix_command(
            "nix-instantiate",
            self.nix_path_arguments() + ["--eval", "--expr", expression],
        )
        # cut off the last newline character append to the output
        return output[:-1]

    def shell(self, command, derivation_path, nix_arguments={}):
        output = self.run_nix_command(
            "nix-shell",
            create_command_options(nix_arguments, list_form=True)
            + [derivation_path, "--command", command],
        )
        return output

    def run_nix_command(self, binary_name, command):
        final_command = (
            [self.executable_path(binary_name)] + self.nix_path_arguments() + command
        )
        try:
            returncode, output = cmd(final_command, verbose=self.verbose)
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

    def nix_path_arguments(self):
        path_arguments = []
        for path in self.nix_path:
            path_arguments.append("-I")
            path_arguments.append(path)
        return path_arguments

    def executable_path(self, program_name):
        if self.executable_directory is None:
            return program_name
        else:
            return os.path.join(self.executable_directory, program_name)
