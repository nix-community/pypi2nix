import glob
import json
import os
import sys
import urllib

import click
import pypi2nix.utils
from pypi2nix.nix import EvaluationFailed
from pypi2nix.utils import escape_double_quotes

HERE = os.path.dirname(__file__)
PIP_NIX = os.path.join(os.path.dirname(__file__), "pip.nix")


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
        self.build_output = None

    def build(self):
        self.evaluate_environment_variables()
        nix_arguments = dict(
            requirements_files=self.requirements_files,
            project_dir=self.project_dir,
            download_cache_dir=self.download_cache_dir,
            wheel_cache_dir=self.wheel_cache_dir,
            extra_build_inputs=self.extra_build_inputs,
            extra_env=self.evaluated_environment,
            python_version=self.python_version,
            setup_requires=self.setup_requires,
            wheels_cache=self.wheels_cache,
        )

        try:
            self.build_output = self.nix.shell(
                command="exit", derivation_path=PIP_NIX, nix_arguments=nix_arguments
            )
        except EvaluationFailed as error:
            self.build_output = error.output
            self.handle_build_error()
        else:
            if self.build_output.endswith("ERROR: Failed to build one or more wheels"):
                self.handle_build_error()

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

    def handle_build_error(self):
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
