import os
import os.path
import sys

from pypi2nix.configuration import ApplicationConfiguration
from pypi2nix.logger import Logger
from pypi2nix.logger import StreamLogger
from pypi2nix.memoize import memoize
from pypi2nix.nix import Nix
from pypi2nix.pip.implementation import NixPip
from pypi2nix.pypi import Pypi
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements_collector import RequirementsCollector
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.stage3 import main
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.version import pypi2nix_version


class Pypi2nix:
    def __init__(self, configuration: ApplicationConfiguration) -> None:
        self.configuration = configuration

    def run(self) -> None:
        requirements = self.requirements_collector().requirements()
        self.logger().info("pypi2nix v{} running ...".format(pypi2nix_version))
        if not requirements:
            self.logger().info("No requirements were specified.  Ending program.")
            return

        setup_requirements = self.setup_requirements_collector().requirements()
        requirements_name = os.path.join(
            self.configuration.target_directory, self.configuration.output_basename
        )

        sources = Sources()
        sources.update(setup_requirements.sources())
        sources.update(requirements.sources())
        sources.update(self.setup_requirements_collector().sources())
        sources.update(self.requirements_collector().sources())

        self.logger().info("Downloading wheels and creating wheelhouse ...")

        pip = NixPip(
            nix=self.nix(),
            project_directory=self.configuration.project_directory,
            extra_env=self.configuration.extra_environment,
            extra_build_inputs=self.configuration.extra_build_inputs,
            wheels_cache=self.configuration.wheels_caches,
            target_platform=self.target_platform(),
            logger=self.logger(),
            requirement_parser=self.requirement_parser(),
        )
        wheel_builder = WheelBuilder(
            pip=pip,
            project_directory=self.configuration.project_directory,
            logger=self.logger(),
            requirement_parser=self.requirement_parser(),
            target_platform=self.target_platform(),
        )
        wheels = wheel_builder.build(
            requirements=requirements, setup_requirements=setup_requirements
        )
        requirements_frozen = wheel_builder.get_frozen_requirements()
        additional_dependency_graph = wheel_builder.additional_build_dependencies

        self.logger().info("Extracting metadata from pypi.python.org ...")

        stage2 = Stage2(
            sources=sources,
            logger=self.logger(),
            requirement_parser=self.requirement_parser(),
            pypi=Pypi(logger=self.logger()),
        )

        packages_metadata = stage2.main(
            wheel_paths=wheels,
            target_platform=self.target_platform(),
            additional_dependencies=additional_dependency_graph,
        )
        self.logger().info("Generating Nix expressions ...")

        main(
            packages_metadata=packages_metadata,
            sources=sources,
            requirements_name=requirements_name,
            requirements_frozen=requirements_frozen,
            extra_build_inputs=(
                self.configuration.extra_build_inputs
                if self.configuration.emit_extra_build_inputs
                else []
            ),
            enable_tests=self.configuration.enable_tests,
            python_version=self.configuration.python_version,
            target_directory=self.configuration.target_directory,
            logger=self.logger(),
            common_overrides=self.configuration.overrides,
        )
        self.print_user_information()

    def print_user_information(self) -> None:
        self.logger().info(
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

    @memoize
    def requirements_collector(self) -> RequirementsCollector:
        requirement_collector = RequirementsCollector(
            self.target_platform(),
            self.requirement_parser(),
            self.logger(),
            self.configuration.project_directory,
        )
        for item in self.configuration.requirements:
            requirement_collector.add_line(item)
        for requirement_file_path in self.configuration.requirement_files:
            requirement_collector.add_file(requirement_file_path)
        return requirement_collector

    @memoize
    def setup_requirements_collector(self) -> RequirementsCollector:
        setup_requirement_collector = RequirementsCollector(
            self.target_platform(),
            self.requirement_parser(),
            self.logger(),
            self.configuration.project_directory,
        )
        for build_input in self.configuration.setup_requirements:
            setup_requirement_collector.add_line(build_input)
        return setup_requirement_collector

    @memoize
    def requirement_parser(self) -> RequirementParser:
        return RequirementParser(self.logger())

    @memoize
    def target_platform(self) -> TargetPlatform:
        platform_generator = PlatformGenerator(nix=self.nix())
        target_platform = platform_generator.from_python_version(
            self.configuration.python_version
        )
        return target_platform

    @memoize
    def nix(self) -> Nix:
        return Nix(
            nix_path=self.configuration.nix_path,
            executable_directory=self.configuration.nix_executable_directory,
            logger=self.logger(),
        )

    @memoize
    def logger(self) -> Logger:
        logger: Logger = StreamLogger(output=sys.stdout)
        logger.set_verbosity(self.configuration.verbosity)
        return logger
