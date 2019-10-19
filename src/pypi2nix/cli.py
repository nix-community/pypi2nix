import os
import os.path
from typing import List
from typing import Optional

import click

from pypi2nix.configuration import ApplicationConfiguration
from pypi2nix.logger import verbosity_from_int
from pypi2nix.main import Pypi2nix
from pypi2nix.overrides import OVERRIDES_URL
from pypi2nix.overrides import Overrides
from pypi2nix.overrides import OverridesGithub
from pypi2nix.project_directory import PersistentProjectDirectory
from pypi2nix.project_directory import ProjectDirectory
from pypi2nix.project_directory import TemporaryProjectDirectory
from pypi2nix.python_version import PythonVersion
from pypi2nix.python_version import available_python_versions
from pypi2nix.utils import args_as_list
from pypi2nix.version import pypi2nix_version


@click.command("pypi2nix")
@click.option("--version", is_flag=True, help="Show version of pypi2nix")
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
@click.option(
    "-I",
    "--nix-path",
    multiple=True,
    default=None,
    help="Add a path to the Nix expression search path. This "
    "option may be given multiple times. See the NIX_PATH "
    "environment variable for information on the semantics "
    "of the Nix search path. Paths added through -I take "
    "precedence over NIX_PATH.",
)
@click.option(
    "--nix-shell", required=False, default=None, help="Path to nix-shell executable."
)
@click.option(
    "--basename",
    required=False,
    default="requirements",
    help="Basename which is used to generate files. By default "
    "it uses basename of provided file.",
)
@click.option(
    "-E",
    "--extra-build-inputs",
    multiple=True,
    default=None,
    help="Extra build dependencies needed for installation of "
    "required python packages.",
)
@click.option(
    "--emit-extra-build-inputs/--no-emit-extra-build-inputs",
    default=True,
    help="Put extra build dependencies (specified using -E) in generated output.",
)
@click.option(
    "-N",
    "--extra-env",
    default="",
    help="Extra environment variables needed for installation of "
    "required python packages."
    'Example: "LANG=en_US.UTF-8 FOO_OPTS=xyz"',
)
@click.option(
    "-T", "--enable-tests", is_flag=True, help="Enable tests in generated packages."
)
@click.option(
    "-V",
    "--python-version",
    "python_version_argument",
    required=False,
    default="python3",
    type=click.Choice(available_python_versions),
    show_default=True,
    help="Provide which python version we build for.",
)
@click.option(
    "-r",
    "--requirements",
    required=False,
    default=[],
    multiple=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="pip requirements.txt file",
)
@click.option(
    "-e",
    "--editable",
    multiple=True,
    required=False,
    default=[],
    type=str,
    help="location/url to editable locations",
)
@click.option(
    "-s",
    "--setup-requires",
    multiple=True,
    required=False,
    default=None,
    type=str,
    help="Extra Python dependencies needed before the installation " "to build wheels.",
)
@click.option(
    "-O",
    "--overrides",
    multiple=True,
    required=False,
    type=OVERRIDES_URL,
    help="Extra expressions that override generated expressions "
    + "for specific packages",
)
@click.option(
    "--default-overrides/--no-default-overrides",
    default=True,
    help='Apply overrides from "nixpkgs-python" (https://github.com/nix-community/pypi2nix-overrides)',  # noqa
)
@click.option(
    "-W",
    "--wheels-cache",
    multiple=True,
    required=False,
    default=[],
    type=str,
    help="An url where trusted wheels are located. eg. https://travis.garbas.si/wheels-cache",  # noqa
)
@click.option(
    "--build-directory",
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help=" ".join(
        [
            "WARNING: This option does not work, don't use it.",
            "Directory where pypi2nix stores all build artifacts,",
            "if not specified a temporary directory will be used",
        ]
    ),
)
def main(
    version: str,
    verbose: int,
    quiet: int,
    nix_shell: Optional[str],
    nix_path: List[str],
    basename: str,
    extra_build_inputs: List[str],
    emit_extra_build_inputs: bool,
    extra_env: str,
    enable_tests: bool,
    python_version_argument: str,
    requirements: List[str],
    editable: List[str],
    setup_requires: List[str],
    overrides: List[Overrides],
    default_overrides: bool,
    wheels_cache: List[str],
    build_directory: Optional[str],
) -> None:
    if version:
        click.echo(pypi2nix_version)
        exit(0)
    verbosity = verbosity_from_int(verbose - quiet + DEFAULT_VERBOSITY)
    nix_executable_directory: Optional[str]
    if nix_shell is None:
        nix_executable_directory = None
    else:
        if not os.path.isfile(nix_shell):
            raise click.exceptions.UsageError(
                f"Specified `nix-shell` executable `{nix_shell}` does not exist."
            )
        else:
            nix_executable_directory = os.path.dirname(os.path.abspath(nix_shell))

    if default_overrides:
        overrides += tuple(
            [
                OverridesGithub(
                    owner="nix-community",
                    repo="pypi2nix-overrides",
                    path="overrides.nix",
                )
            ]
        )
    python_version = getattr(PythonVersion, python_version_argument, None)
    if python_version is None:
        raise click.exceptions.UsageError(
            f"Python version `{python_version_argument}` not available"
        )

    project_directory_context: ProjectDirectory = (
        TemporaryProjectDirectory()
        if build_directory is None
        else PersistentProjectDirectory(path=build_directory)
    )
    with project_directory_context as _project_directory:
        configuration = ApplicationConfiguration(
            emit_extra_build_inputs=emit_extra_build_inputs,
            enable_tests=enable_tests,
            extra_build_inputs=args_as_list(extra_build_inputs),
            extra_environment=extra_env,
            nix_executable_directory=nix_executable_directory,
            nix_path=nix_path,
            output_basename=basename,
            overrides=overrides,
            python_version=python_version,
            requirement_files=requirements,
            requirements=editable,
            setup_requirements=setup_requires,
            verbosity=verbosity,
            wheels_caches=wheels_cache,
            project_directory=_project_directory,
            target_directory=os.getcwd(),
        )
        Pypi2nix(configuration).run()


DEFAULT_VERBOSITY = 1
