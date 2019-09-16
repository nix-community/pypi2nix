#!/usr/bin/env python
"This script prepares the test fixtures for the unittests of this package"

import os
import os.path
import shutil
import subprocess
import sys
import tempfile
import venv

from build_wheel import build_wheel
from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import PlatformGenerator
from repository import ROOT

wheel_target_directory = os.path.join(ROOT, "unittests", "data")


def package_setupcfg_package():
    package_dir = os.path.join(ROOT, "unittests", "data", "setupcfg-package")
    paths_to_delete = ["setupcfg_package.egg-info", "dist", "setupcfg-package.tar.gz"]
    for path in paths_to_delete:
        shutil.rmtree(os.path.join(package_dir, "path"), ignore_errors=True)
    subprocess.run(["python", "setup.py", "sdist"], cwd=package_dir, check=True)
    shutil.copy(
        os.path.join(package_dir, "dist", "setupcfg-package-1.0.tar.gz"),
        wheel_target_directory,
    )
    shutil.move(
        os.path.join(package_dir, "dist", "setupcfg-package-1.0.tar.gz"),
        os.path.join(package_dir, "setupcfg-package.tar.gz"),
    )
    build_wheel(wheel_target_directory, package_dir)


def download_setupcfg_dependencies():
    logger = StreamLogger(sys.stdout)
    nix = Nix(logger)
    platform = PlatformGenerator(nix).current_platform()
    if platform is None:
        logger.error("Could not determin current platform, exiting")
        exit(1)
    requirement_parser = RequirementParser(logger)
    requirements = RequirementSet(platform)
    requirements.add(requirement_parser.parse("requests"))
    requirements.add(requirement_parser.parse("pytest"))

    with tempfile.TemporaryDirectory() as directory:
        target_directory = os.path.join(directory, "test_data_env")
        env_builder = venv.EnvBuilder(with_pip=True)
        pip = VirtualenvPip(logger, platform, target_directory, env_builder)
        pip.prepare_virtualenv()
        pip.download_sources(requirements, wheel_target_directory)


if __name__ == "__main__":
    download_setupcfg_dependencies()
    package_setupcfg_package()
