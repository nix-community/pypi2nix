import os
import shutil
import sys
import tempfile
from typing import List
from typing import Optional

import click

import pypi2nix.overrides
import pypi2nix.stage1
import pypi2nix.stage2
import pypi2nix.stage3
import pypi2nix.utils
from pypi2nix.logger import Logger
from pypi2nix.nix import Nix
from pypi2nix.overrides import AnyOverrides
from pypi2nix.pip import Pip
from pypi2nix.requirements_collector import RequirementsCollector
from pypi2nix.sources import Sources
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.utils import md5_sum_of_files_with_file_names


@click.command("pypi2nix")
@click.option("--version", is_flag=True, help=u"Show version of pypi2nix")
@click.option("-v", "--verbose", count=True)
@click.option(
    "-I",
    "--nix-path",
    multiple=True,
    default=None,
    help=u"Add a path to the Nix expression search path. This "
    u"option may be given multiple times. See the NIX_PATH "
    u"environment variable for information on the semantics "
    u"of the Nix search path. Paths added through -I take "
    u"precedence over NIX_PATH.",
)
@click.option(
    "--nix-shell",
    required=False,
    default="nix-shell",
    help=u"Path to nix-shell executable.",
)
@click.option(
    "--basename",
    required=False,
    default="requirements",
    help=u"Basename which is used to generate files. By default "
    u"it uses basename of provided file.",
)
@click.option(
    "-C",
    "--cache-dir",
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, writable=True, resolve_path=True),
    help=u"Cache directory to be used for downloading packages.",
)
@click.option(
    "-E",
    "--extra-build-inputs",
    multiple=True,
    default=None,
    help=u"Extra build dependencies needed for installation of "
    u"required python packages.",
)
@click.option(
    "-N",
    "--extra-env",
    default="",
    help=u"Extra environment variables needed for installation of "
    u"required python packages."
    u'Example: "LANG=en_US.UTF-8 FOO_OPTS=xyz"',
)
@click.option(
    "-T", "--enable-tests", is_flag=True, help=u"Enable tests in generated packages."
)
@click.option(
    "-V",
    "--python-version",
    required=False,
    default=None,
    type=click.Choice(pypi2nix.utils.PYTHON_VERSIONS.keys()),
    help=u"Provide which python version we build for.",
)
@click.option(
    "-r",
    "--requirements",
    required=False,
    default=[],
    multiple=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help=u"pip requirements.txt file",
)
@click.option(
    "-e",
    "--editable",
    multiple=True,
    required=False,
    default=[],
    type=str,
    help=u"location/url to editable locations",
)
@click.option(
    "-s",
    "--setup-requires",
    multiple=True,
    required=False,
    default=None,
    type=str,
    help=u"Extra Python dependencies needed before the installation "
    u"to build wheels.",
)
@click.option(
    "-O",
    "--overrides",
    multiple=True,
    required=False,
    type=pypi2nix.overrides.OVERRIDES_URL,
    help=u"Extra expressions that override generated expressions "
    + u"for specific packages",
)
@click.option(
    "--default-overrides/--no-default-overrides",
    default=False,
    help=u'Apply overrides from "nixpkgs-python" (https://github.com/garbas/nixpkgs-python)',  # noqa
)
@click.option(
    "-W",
    "--wheels-cache",
    multiple=True,
    required=False,
    default=[],
    type=str,
    help=u"An url where trusted wheels are located. eg. https://travis.garbas.si/wheels-cache",  # noqa
)
def main(
    version: str,
    verbose: int,
    nix_shell: str,
    nix_path: List[str],
    basename: str,
    cache_dir: str,
    extra_build_inputs: List[str],
    extra_env: str,
    enable_tests: bool,
    python_version: str,
    requirements: List[str],
    editable: List[str],
    setup_requires: List[str],
    overrides: List[AnyOverrides],
    default_overrides: bool,
    wheels_cache: List[str],
) -> None:
    """SPECIFICATION should be requirements.txt (output of pip freeze).
    """

    logger = Logger(output=sys.stdout)
    nix_executable_directory: Optional[str] = (
        os.path.abspath(os.path.dirname(nix_shell))
        if os.path.exists(nix_shell)
        else None
    )

    nix = Nix(
        nix_path=nix_path,
        executable_directory=nix_executable_directory,
        verbose=verbose != 0,
    )
    platform_generator = PlatformGenerator(nix=nix)

    if default_overrides:
        overrides += tuple(
            [
                pypi2nix.overrides.OverridesGithub(
                    owner="garbas", repo="nixpkgs-python", path="overrides.nix"
                )
            ]
        )

    with open(os.path.join(os.path.dirname(__file__), "VERSION")) as f:
        pypi2nix_version = f.read()

    if version:
        click.echo(pypi2nix_version)
        return

    python_version_argument = python_version
    python_versions = pypi2nix.utils.PYTHON_VERSIONS.keys()
    if not python_version:
        raise click.exceptions.UsageError(
            'Missing option "-V" / "--python-version".  Choose from '
            + (", ".join(python_versions))
        )
    python_version = pypi2nix.utils.PYTHON_VERSIONS[python_version]
    target_platform = platform_generator.from_python_version(python_version_argument)

    requirement_collector = RequirementsCollector(target_platform)
    setup_requirement_collector = RequirementsCollector(target_platform)

    extra_build_inputs = pypi2nix.utils.args_as_list(extra_build_inputs)
    setup_requires = pypi2nix.utils.args_as_list(setup_requires)

    for item in editable:
        requirement_collector.add_line(item)
    for build_input in setup_requires:
        setup_requirement_collector.add_line(build_input)

    # temporary pypi2nix folder and make sure it exists
    tmp_dir = os.path.join(tempfile.gettempdir(), "pypi2nix")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    current_dir = os.getcwd()
    requirements_name = os.path.join(current_dir, basename)

    if not cache_dir:
        cache_dir = os.path.join(tmp_dir, "cache")

    download_cache_dir = os.path.join(cache_dir, "download")
    wheel_cache_dir = os.path.join(cache_dir, "wheel")

    if not os.path.exists(download_cache_dir):
        os.makedirs(download_cache_dir)

    if not os.path.exists(wheel_cache_dir):
        os.makedirs(wheel_cache_dir)

    assert requirements is not None

    project_hash = md5_sum_of_files_with_file_names(requirements)

    project_dir = os.path.join(tmp_dir, project_hash)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)

    for requirement_file_path in requirements:
        requirement_collector.add_file(requirement_file_path)

    requirement_set = requirement_collector.requirements()
    setup_requirements = setup_requirement_collector.requirements()

    sources = Sources()
    sources.update(requirement_set.sources())
    sources.update(setup_requirements.sources())

    click.echo("pypi2nix v{} running ...".format(pypi2nix_version))
    click.echo("")

    click.echo("Stage1: Downloading wheels and creating wheelhouse ...")

    pip = Pip(
        nix=nix,
        project_directory=project_dir,
        extra_env=extra_env,
        extra_build_inputs=extra_build_inputs,
        verbose=verbose,
        wheels_cache=wheels_cache,
        target_platform=target_platform,
    )
    wheel_builder = pypi2nix.stage1.WheelBuilder(
        pip=pip, project_directory=project_dir, logger=logger
    )
    wheels = wheel_builder.build(
        requirements=requirement_set, setup_requirements=setup_requirements
    )
    requirements_frozen = wheel_builder.get_frozen_requirements()
    default_environment = pip.default_environment()
    additional_dependency_graph = wheel_builder.additional_build_dependencies

    click.echo("Stage2: Extracting metadata from pypi.python.org ...")

    stage2 = pypi2nix.stage2.Stage2(sources=sources, verbose=verbose)

    packages_metadata = stage2.main(
        wheel_paths=wheels,
        default_environment=default_environment,
        wheel_cache_dir=wheel_cache_dir,
        additional_dependencies=additional_dependency_graph,
    )
    click.echo("Stage3: Generating Nix expressions ...")

    pypi2nix.stage3.main(
        packages_metadata=packages_metadata,
        sources=sources,
        requirements_name=requirements_name,
        requirements_frozen=requirements_frozen,
        extra_build_inputs=extra_build_inputs,
        enable_tests=enable_tests,
        python_version=python_version,
        current_dir=current_dir,
        common_overrides=overrides,
    )

    click.echo("")
    click.echo("Nix expressions generated successfully.")
    click.echo("")
    click.echo("To start development run:")
    click.echo("    nix-shell requirements.nix -A interpreter")
    click.echo("")
    click.echo("More information you can find at")
    click.echo("    https://github.com/nix-community/pypi2nix")
    click.echo("")
