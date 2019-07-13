import os
import os.path
import shutil
import subprocess

from attr import attrib
from attr import attrs
from attr import evolve

from pypi2nix.nix import EvaluationFailed
from pypi2nix.nix import Nix

HERE = os.path.dirname(__file__)
NIX_PATH = (
    "nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixpkgs-unstable.tar.gz"
)


class IntegrationTest:
    """Methods to implement for a valid test case:

    name_of_testcase()
    requirements()
    python_version()

    optional:

    code_for_testing() -- default: []
    code_for_testing_filename() -- default: None
    setup_requires() -- default: []
    executables_for_testing() -- default: []
    extra_environment() -- default: dict()
    external_dependencies() -- default: []
    default_overrides -- default: false
    requirements_file_check(content) -- default: (lambda content: None)
    constraints -- default []
    """

    def setUp(self):
        self.nix = Nix(nix_path=[NIX_PATH], verbose=True)

    def test_build_example(self):
        self.build_pypi2nix()
        self.generate_requirements_file()
        self.build_nix_expression()
        self.check_requirements_file_content()
        self.run_expression_tests()

    def build_pypi2nix(self):
        print("Build pypi2nix executable")
        try:
            self.nix.build(
                os.path.join(os.path.dirname(HERE), "default.nix"),
                arguments={"excludeIntegrationTests": True},
                out_link=os.path.join(HERE, "pypi2nix"),
            )
        except EvaluationFailed:
            self.fail("Could not build pypi2nix executable")

    def generate_requirements_file(self):
        print("Generate requirements.txt")
        requirements_file_content = self.generate_requirements_file_content()
        self.write_requirements_file(requirements_file_content)

    def build_nix_expression(self):
        print("Build nix expression")
        process = subprocess.Popen(
            self.build_nix_expression_command(),
            cwd=self.example_directory(),
            env=self.nix_build_env(),
            stdin=subprocess.DEVNULL,
        )
        process.communicate()
        if process.returncode != 0:
            self.fail(
                "Could not build nix expression for {testname}".format(
                    testname=self.name_of_testcase()
                )
            )

    def build_nix_expression_command(self):
        command = [
            os.path.join(HERE, "pypi2nix", "bin", "pypi2nix"),
            "-vvv",
            "-V",
            self.python_version(),
            "-r",
            "requirements.txt",
        ]
        for requirement in self.setup_requires():
            command.append("-s")
            command.append(requirement)

        for variable_name, value in self.extra_environment().items():
            command.append("-N")
            command.append("{name}={value}".format(name=variable_name, value=value))

        for dependency in self.external_dependencies():
            command.append("-E")
            command.append(dependency)

        if self.default_overrides:
            command.append("--default-overrides")

        return command

    def setup_requires(self):
        return []

    def check_requirements_file_content(self):
        requirements_file_content = self.read_requirements_file_contents()
        self.requirements_file_check(requirements_file_content)

    def run_expression_tests(self):
        self.build_interpreter_from_generated_expression()
        self.run_interpreter_with_test_code()
        self.run_executable_tests()

    def build_interpreter_from_generated_expression(self):
        print("Build python interpreter from generated expression")
        try:
            self.nix.build(
                os.path.join(self.example_directory(), "requirements.nix"),
                attribute="interpreter",
                out_link=os.path.join(self.example_directory(), "result"),
            )
        except EvaluationFailed:
            self.fail(
                "Failed to build python interpreter from nix expression generated"
            )

    def run_interpreter_with_test_code(self):
        if self.code_for_testing_string():
            test_code = self.code_for_testing_string()
            self.run_interpreter_with_test_code_from_result(test_code)
            self.run_interpreter_with_test_code_in_nix_shell(test_code)

    def run_interpreter_with_test_code_from_result(self, test_code):
        print("Run generated interpreter with test code")
        process = subprocess.Popen(
            [os.path.join(self.example_directory(), "result", "bin", "python")],
            stdin=subprocess.PIPE,
        )
        process.communicate(input=test_code.encode())
        if process.returncode != 0:
            self.fail("Executation of test code failed")

    def run_interpreter_with_test_code_in_nix_shell(self, test_code):
        print("Execute test code in nix-shell")
        test_command_line = [
            "nix",
            "run",
            "-f",
            os.path.join(self.example_directory(), "requirements.nix"),
            "interpreter",
            "--command",
            "python",
        ]
        process = subprocess.Popen(
            test_command_line,
            cwd=os.path.join(self.example_directory(), "result", "bin"),
            env=self.nix_build_env(),
            stdin=subprocess.PIPE,
        )
        process.communicate(input=test_code.encode())
        if process.returncode != 0:
            self.fail("Executation of test code in nix-shell failed")

    def read_requirements_file_contents(self):
        with open(os.path.join(self.example_directory(), "requirements.nix")) as f:
            return f.read()

    def code_for_testing_string(self):
        if self.code_for_testing() and self.code_for_testing_filename():
            self.fail(
                "Cannot set `both code_for_testing` and `code_for_testing_filename`."
            )
        if self.code_for_testing():
            return "\n".join(self.code_for_testing())
        if self.code_for_testing_filename():
            with open(
                os.path.join(self.example_directory(), self.code_for_testing_filename)
            ) as f:
                return f.read().splitlines()

    def code_for_testing(self):
        return []

    def code_for_testing_filename(self):
        return

    def extra_environment(self):
        return dict()

    def external_dependencies(self):
        return []

    def run_executable_tests(self):
        for test_command in self.executables_for_testing():
            self.run_test_command_in_shell(test_command)
            self.run_test_command_from_build_output(test_command)

    def run_test_command_in_shell(self, test_command):
        print("Run {command} in nix-shell".format(command=test_command))
        test_command_line = [
            "nix",
            "run",
            "-f",
            os.path.join(self.example_directory(), "requirements.nix"),
            "interpreter",
            "--command",
        ] + test_command.command
        process = subprocess.Popen(
            test_command_line,
            cwd=os.path.join(self.example_directory(), "result", "bin"),
            env=dict(self.nix_build_env(), **test_command.env),
        )
        process.communicate()
        print()  # for empty line after command output
        if process.returncode != 0:
            self.fail(
                "Tested executable `{command}` returned non-zero exitcode.".format(
                    command=test_command
                )
            )

    def run_test_command_from_build_output(self, test_command):
        prepared_test_command = evolve(
            test_command,
            command=["./" + test_command.command[0]] + test_command.command[1:],
        )
        print("Run {command}".format(command=prepared_test_command))
        process = subprocess.Popen(
            prepared_test_command.command,
            cwd=os.path.join(self.example_directory(), "result", "bin"),
            env=dict(self.nix_build_env(), **prepared_test_command.env),
        )
        process.communicate()
        print()  # for empty line after command output
        if process.returncode != 0:
            self.fail(
                "Tested executable `{command}` returned non-zero exitcode.".format(
                    command=test_command
                )
            )

    def executables_for_testing(self):
        return []

    def nix_build_env(self):
        environment_variables = dict(os.environ)
        environment_variables["NIX_PATH"] = NIX_PATH
        return environment_variables

    def generate_requirements_file_content(self):
        if self.constraints:
            self.generate_constraints_txt()
            requirements_txt_extra_content = ["-c " + self.constraints_txt_path()]
        else:
            requirements_txt_extra_content = []
        return "\n".join(self.requirements() + requirements_txt_extra_content)

    def generate_constraints_txt(self):
        with open(self.constraints_txt_path(), "w") as f:
            f.write("\n".join(self.constraints))

    def constraints_txt_path(self):
        return os.path.join(self.example_directory(), "constraints.txt")

    def write_requirements_file(self, content):
        shutil.os.makedirs(
            os.path.dirname(self.requirements_file_path()), exist_ok=True
        )
        with open(self.requirements_file_path(), "w") as f:
            f.write(content)

    def requirements_file_path(self):
        return os.path.join(self.example_directory(), "requirements.txt")

    def example_directory(self):
        return os.path.join(HERE, self.name_of_testcase())

    def requirements_file_check(self, _):
        pass

    default_overrides = False
    constraints = []


@attrs
class TestCommand:
    command = attrib()
    env = attrib(default=dict())
