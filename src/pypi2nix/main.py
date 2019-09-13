import os
import os.path
import shutil
import sys
import tempfile

from pypi2nix.configuration import ApplicationConfiguration
from pypi2nix.logger import Logger
from pypi2nix.logger import StreamLogger
from pypi2nix.memoize import memoize
from pypi2nix.nix import Nix
from pypi2nix.pip.implementation import NixPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements_collector import RequirementsCollector
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.stage3 import main
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.utils import md5_sum_of_files_with_file_names
from pypi2nix.version import pypi2nix_version


class Pypi2nix:
    def __init__(self, configuration: ApplicationConfiguration) -> None:
        self.configuration = configuration

    def run(self) -> None:
        self.logger().info("pypi2nix v{} running ...".format(pypi2nix_version))
        if not self.requirements():
            self.logger().info("No requirements were specified.  Ending program.")
            return

        project_dir = self.set_up_project_directory()
        current_dir = os.getcwd()
        requirements_name = os.path.join(current_dir, self.configuration.basename)

        sources = Sources()
        sources.update(self.requirements().sources())
        sources.update(self.setup_requirements().sources())

        self.logger().info("Downloading wheels and creating wheelhouse ...")

        pip = NixPip(
            nix=self.nix(),
            project_directory=project_dir,
            extra_env=self.configuration.extra_environment,
            extra_build_inputs=self.configuration.extra_build_inputs,
            wheels_cache=self.configuration.wheels_caches,
            target_platform=self.target_platform(),
            logger=self.logger(),
        )
        wheel_builder = WheelBuilder(
            pip=pip,
            project_directory=project_dir,
            logger=self.logger(),
            requirement_parser=self.requirement_parser(),
            target_platform=self.target_platform(),
        )
        wheels = wheel_builder.build(
            requirements=self.requirements(),
            setup_requirements=self.setup_requirements(),
        )
        requirements_frozen = wheel_builder.get_frozen_requirements()
        additional_dependency_graph = wheel_builder.additional_build_dependencies

        self.logger().info("Extracting metadata from pypi.python.org ...")

        stage2 = Stage2(
            sources=sources,
            logger=self.logger(),
            requirement_parser=self.requirement_parser(),
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
            current_dir=current_dir,
            logger=self.logger(),
            common_overrides=self.configuration.overrides,
        )

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

    def set_up_project_directory(self) -> str:
        tmp_dir = os.path.join(tempfile.gettempdir(), "pypi2nix")
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        project_hash = md5_sum_of_files_with_file_names(
            self.configuration.requirement_files
        )
        project_dir = os.path.join(tmp_dir, project_hash)

        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        os.makedirs(project_dir)
        return project_dir

    @memoize
    def requirements(self) -> RequirementSet:
        requirement_collector = RequirementsCollector(
            self.target_platform(), self.requirement_parser()
        )
        for item in self.configuration.requirements:
            requirement_collector.add_line(item)
        for requirement_file_path in self.configuration.requirement_files:
            requirement_collector.add_file(requirement_file_path)
        return requirement_collector.requirements()

    @memoize
    def setup_requirements(self) -> RequirementSet:
        setup_requirement_collector = RequirementsCollector(
            self.target_platform(), self.requirement_parser()
        )
        for build_input in self.configuration.setup_requirements:
            setup_requirement_collector.add_line(build_input)
        return setup_requirement_collector.requirements()

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
