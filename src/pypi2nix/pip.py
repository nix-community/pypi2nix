import json
import os.path
import shutil
import sys
import urllib

import click
from pypi2nix.nix import EvaluationFailed
from pypi2nix.utils import escape_double_quotes

HERE = os.path.dirname(__file__)
DOWNLOAD_NIX = os.path.join(HERE, "pip", "download.nix")
WHEEL_NIX = os.path.join(HERE, "pip", "wheel.nix")
INSTALL_NIX = os.path.join(HERE, "pip", "install.nix")
BASE_NIX = os.path.join(HERE, "pip", "base.nix")


class Pip:
    def __init__(
        self,
        nix,
        project_directory,
        extra_build_inputs,
        python_version,
        extra_env,
        verbose: int,
        wheels_cache,
    ):
        self.nix = nix
        self.project_directory = project_directory
        self.extra_build_inputs = extra_build_inputs
        self.python_version = python_version
        self.extra_env = extra_env
        self.build_output = ""
        self.verbose = verbose
        self.wheels_cache = wheels_cache

        output = self.nix.evaluate_expression(
            'let pkgs = import <nixpkgs> {}; in "%s"' % escape_double_quotes(extra_env)
        )
        # trim quotes
        self.extra_env = output[1:-1]

        self.wheel_cache_dir = os.path.join(self.project_directory, "cache", "wheels")
        self.download_cache_directory = os.path.join(
            self.project_directory, "cache", "download"
        )

    def download_sources(self, requirements, target_directory, constraints=[]):
        requirements_files = list(
            map(lambda r: r.processed_requirements_file_path(), requirements)
        )
        constraints_files = list(
            map(lambda c: c.processed_requirements_file_path(), constraints)
        )
        with open(requirements_files[0]) as f:
            print(f.read())
        self.build_from_nix_file(
            command="exit",
            file_path=DOWNLOAD_NIX,
            nix_arguments=self.nix_arguments(
                requirements_files=requirements_files,
                destination_directory=target_directory,
                editable_sources_directory=self.editable_sources_directory(),
                build_directory=self.build_directory(),
                constraint_files=constraints_files,
            ),
        )

    def build_wheels(
        self, requirements, target_directory, source_directories, constraints=[]
    ):
        requirements_files = list(
            map(lambda r: r.processed_requirements_file_path(), requirements)
        )
        self.build_from_nix_file(
            command="exit",
            file_path=WHEEL_NIX,
            nix_arguments=self.nix_arguments(
                wheels_cache=self.wheels_cache,
                requirements_files=requirements_files,
                wheel_cache_dir=self.wheel_cache_dir,
                editable_sources_directory=self.editable_sources_directory(),
                build_directory=self.build_directory(),
                wheels_dir=target_directory,
                sources=source_directories,
            ),
        )

    def install(self, requirements, source_directories):
        requirements_files = list(
            map(lambda r: r.processed_requirements_file_path(), requirements)
        )
        self.build_from_nix_file(
            command="exit",
            file_path=INSTALL_NIX,
            nix_arguments=self.nix_arguments(
                requirements_files=requirements_files,
                wheel_cache_dir=self.wheel_cache_dir,
                target_directory=os.path.join(self.project_directory, "lib"),
                sources_directories=source_directories,
            ),
        )

    def freeze(self):
        output = self.nix.shell(
            "pip freeze", BASE_NIX, nix_arguments=self.nix_arguments()
        )
        return "\n".join(map(lambda x: x.strip(), output.splitlines()))

    def default_environment(self):
        output = self.nix.shell(
            'python -c "import json; from setuptools._vendor.packaging.markers import default_environment; print(json.dumps(default_environment(), indent=2, sort_keys=True))"',
            BASE_NIX,
            nix_arguments=self.nix_arguments(),
        )
        return json.loads(output)

    def editable_sources_directory(self):
        return os.path.join(self.project_directory, "editable_sources")

    def build_directory(self):
        return os.path.join(self.project_directory, "build")

    def nix_arguments(self, **arguments):
        return dict(
            dict(
                download_cache_dir=self.download_cache_directory,
                extra_build_inputs=self.extra_build_inputs,
                project_dir=self.project_directory,
                python_version=self.python_version,
                extra_env=self.extra_env,
            ),
            **arguments,
        )

    def build_from_nix_file(self, file_path, command, nix_arguments):
        self.create_download_cache_if_missing()
        self.create_wheel_cache_dir_if_missing()
        self.delete_build_directory()
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

    def create_download_cache_if_missing(self):
        if os.path.exists(self.download_cache_directory):
            pass
        else:
            os.makedirs(self.download_cache_directory)

    def create_wheel_cache_dir_if_missing(self):
        if os.path.exists(self.wheel_cache_dir):
            pass
        else:
            os.makedirs(self.wheel_cache_dir)

    def delete_build_directory(self):
        try:
            shutil.rmtree(self.build_directory())
        except FileNotFoundError:
            pass

    def handle_build_error(self, is_failure):
        if not is_failure:
            if not self.build_output.endswith(
                "ERROR: Failed to build one or more wheels"
            ):
                return

        if self.verbose > 0:
            click.echo(self.build_output)

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
