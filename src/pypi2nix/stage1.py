import glob
import json
import os
import shutil
import sys
import urllib
from functools import lru_cache

import click
import pypi2nix.utils
from pypi2nix.nix import EvaluationFailed
from pypi2nix.utils import escape_double_quotes

HERE = os.path.dirname(__file__)
PIP_NIX = os.path.join(HERE, "pip.nix")
DOWNLOAD_NIX = os.path.join(HERE, "pip", "download.nix")
WHEEL_NIX = os.path.join(HERE, "pip", "wheel.nix")
INSTALL_NIX = os.path.join(HERE, "pip", "install.nix")


class WheelBuilder:
    def __init__(
        self,
        requirements_files,
        project_dir,
        download_cache_dir,
        wheel_cache_dir,
        extra_build_inputs,
        python_version,
        nix,
        verbose=0,
        setup_requires=[],
        extra_env="",
        wheels_cache=[],
    ):
        self.verbose = verbose
        self.requirements_files = requirements_files
        self.project_dir = project_dir
        self.download_cache_dir = download_cache_dir
        self.wheel_cache_dir = wheel_cache_dir
        self.extra_build_inputs = extra_build_inputs
        self.python_version = python_version
        self.nix = nix
        self.setup_requires = setup_requires
        self.extra_env = extra_env
        self.wheels_cache = wheels_cache
        self.evaluated_environment = None
        self.build_output = ""

    def build(self):
        self.create_project_directory()
        self.evaluate_environment_variables()
        self.prepare_setup_requirements()
        nix_arguments = dict(
            requirements_files=self.requirements_files,
            project_dir=self.project_dir,
            download_cache_dir=self.download_cache_dir,
            wheel_cache_dir=self.wheel_cache_dir,
            python_version=self.python_version,
            extra_build_inputs=self.extra_build_inputs,
            extra_env=self.evaluated_environment,
            wheels_cache=self.wheels_cache,
        )
        self.build_from_nix_file(
            command="exit", file_path=PIP_NIX, nix_arguments=nix_arguments
        )

    def create_project_directory(self):
        os.makedirs(self.project_dir, exist_ok=True)

    def prepare_setup_requirements(self):
        if self.setup_requires:
            self.download_setup_requirements()
            self.build_setup_requirements()
            self.install_setup_requirements()

    def download_setup_requirements(self):
        self.delete_build_dir()
        nix_arguments = dict(
            download_cache_dir=self.download_cache_dir,
            extra_build_inputs=self.extra_build_inputs,
            project_dir=self.project_dir,
            python_version=self.python_version,
            extra_env=self.evaluated_environment,
            requirements_files=self.setup_requirements_files(),
            constraint_files=self.requirements_files,
        )
        self.build_from_nix_file(
            command="exit", file_path=DOWNLOAD_NIX, nix_arguments=nix_arguments
        )

    def build_setup_requirements(self):
        self.delete_build_dir()
        nix_arguments = dict(
            project_dir=self.project_dir,
            download_cache_dir=self.download_cache_dir,
            python_version=self.python_version,
            extra_build_inputs=self.extra_build_inputs,
            extra_env=self.evaluated_environment,
            wheels_cache=self.wheels_cache,
            requirements_files=self.setup_requirements_files(),
            wheel_cache_dir=self.wheel_cache_dir,
        )
        self.build_from_nix_file(
            command="exit", file_path=WHEEL_NIX, nix_arguments=nix_arguments
        )

    def install_setup_requirements(self):
        nix_arguments = dict(
            project_dir=self.project_dir,
            download_cache_dir=self.download_cache_dir,
            python_version=self.python_version,
            extra_build_inputs=self.extra_build_inputs,
            requirements_files=self.setup_requirements_files(),
            wheel_cache_dir=self.wheel_cache_dir,
            target_directory=os.path.join(self.project_dir, "setup_requires"),
        )
        self.build_from_nix_file(
            command="exit", file_path=INSTALL_NIX, nix_arguments=nix_arguments
        )

    def build_from_nix_file(self, file_path, command, nix_arguments):
        try:
            self.build_output = self.nix.shell(
                command=command, derivation_path=file_path, nix_arguments=nix_arguments
            )
        except EvaluationFailed as error:
            self.build_output += error.output
            is_failure = True
        else:
            is_failure = False
        self.handle_build_error(is_failure=is_failure)

    def delete_build_dir(self):
        build_dir_path = os.path.join(self.project_dir, "build")
        try:
            shutil.rmtree(build_dir_path)
        except FileNotFoundError:
            pass

    @lru_cache()
    def setup_requirements_files(self):
        path = os.path.join(self.project_dir, "setup_requirements.txt")
        with open(path, "w") as requirement_file:
            for requirement in self.setup_requires:
                requirement_file.write(requirement)
                requirement_file.write("\n")
        return [path]

    def default_environment(self):
        with open(os.path.join(self.project_dir, "default_environment.json")) as f:
            return json.load(f)

    def wheels(self):
        return glob.glob(os.path.join(self.project_dir, "wheelhouse", "*.dist-info"))

    def requirements_frozen(self):
        return os.path.join(self.project_dir, "requirements.txt")

    def evaluate_environment_variables(self):
        output = self.nix.evaluate_expression(
            'let pkgs = import <nixpkgs> {}; in "%s"'
            % escape_double_quotes(self.extra_env)
        )
        # trim quotes
        self.evaluated_environment = output[1:-1]

    def handle_build_error(self, is_failure):
        if not is_failure:
            if not self.build_output.endswith(
                "ERROR: Failed to build one or more wheels"
            ):
                return

        if self.verbose == 0:
            click.echo(self.build_output)

        message = u"While trying to run the command something went wrong."

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
                click.echo("Failed to send crash report")

        raise click.ClickException(message)

    def send_crash_report(self):
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
                "https://github.com/garbas/pypi2nix/issues/new?%s"
                % (urllib.parse.urlencode(dict(title=title, body=body)))
            )
