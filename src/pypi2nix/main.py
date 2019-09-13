import os
import os.path
import shutil
import sys
import tempfile

from pypi2nix.configuration import ApplicationConfiguration
from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix
from pypi2nix.pip.implementation import NixPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements_collector import RequirementsCollector
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.stage3 import main
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.utils import md5_sum_of_files_with_file_names
from pypi2nix.version import pypi2nix_version


def run_pypi2nix(configuration: ApplicationConfiguration) -> None:
    logger = StreamLogger(output=sys.stdout)
    logger.set_verbosity(configuration.verbosity)
    requirement_parser = RequirementParser(logger)

    nix = Nix(
        nix_path=configuration.nix_path,
        executable_directory=configuration.nix_executable_directory,
        logger=logger,
    )
    platform_generator = PlatformGenerator(nix=nix)

    target_platform = platform_generator.from_python_version(
        configuration.python_version
    )

    requirement_collector = RequirementsCollector(target_platform, requirement_parser)
    setup_requirement_collector = RequirementsCollector(
        target_platform, requirement_parser
    )

    for item in configuration.requirements:
        requirement_collector.add_line(item)
    for build_input in configuration.setup_requirements:
        setup_requirement_collector.add_line(build_input)

    # temporary pypi2nix folder and make sure it exists
    tmp_dir = os.path.join(tempfile.gettempdir(), "pypi2nix")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    current_dir = os.getcwd()
    requirements_name = os.path.join(current_dir, configuration.basename)

    project_hash = md5_sum_of_files_with_file_names(configuration.requirement_files)

    project_dir = os.path.join(tmp_dir, project_hash)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)

    for requirement_file_path in configuration.requirement_files:
        requirement_collector.add_file(requirement_file_path)

    requirement_set = requirement_collector.requirements()
    setup_requirements = setup_requirement_collector.requirements()

    sources = Sources()
    sources.update(requirement_set.sources())
    sources.update(setup_requirements.sources())

    logger.info("pypi2nix v{} running ...".format(pypi2nix_version))
    logger.info("")

    logger.info("Stage1: Downloading wheels and creating wheelhouse ...")

    pip = NixPip(
        nix=nix,
        project_directory=project_dir,
        extra_env=configuration.extra_environment,
        extra_build_inputs=configuration.extra_build_inputs,
        wheels_cache=configuration.wheels_caches,
        target_platform=target_platform,
        logger=logger,
    )
    wheel_builder = WheelBuilder(
        pip=pip,
        project_directory=project_dir,
        logger=logger,
        requirement_parser=requirement_parser,
        target_platform=target_platform,
    )
    wheels = wheel_builder.build(
        requirements=requirement_set, setup_requirements=setup_requirements
    )
    requirements_frozen = wheel_builder.get_frozen_requirements()
    additional_dependency_graph = wheel_builder.additional_build_dependencies

    logger.info("Stage2: Extracting metadata from pypi.python.org ...")

    stage2 = Stage2(
        sources=sources, logger=logger, requirement_parser=requirement_parser
    )

    packages_metadata = stage2.main(
        wheel_paths=wheels,
        target_platform=target_platform,
        additional_dependencies=additional_dependency_graph,
    )
    logger.info("Stage3: Generating Nix expressions ...")

    main(
        packages_metadata=packages_metadata,
        sources=sources,
        requirements_name=requirements_name,
        requirements_frozen=requirements_frozen,
        extra_build_inputs=(
            configuration.extra_build_inputs
            if configuration.emit_extra_build_inputs
            else []
        ),
        enable_tests=configuration.enable_tests,
        python_version=configuration.python_version,
        current_dir=current_dir,
        logger=logger,
        common_overrides=configuration.overrides,
    )

    logger.info(
        "\n".join(
            [
                "",
                "Nix expressions generated successfully.",
                "",
                "To start development run:",
                "    nix-shell requirements.nix -A interpreter",
                "",
                "More information you can find at",
                "    https://github.com/nix-community/pypi2nix",
                "",
            ]
        )
    )
