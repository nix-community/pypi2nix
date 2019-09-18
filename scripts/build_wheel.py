#!/usr/bin/env python

import os
import shlex
import shutil
import sys
import tempfile

from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix
from repository import ROOT

HERE = os.path.abspath(os.path.dirname(__file__))
DERIVATION_PATH = os.path.join(HERE, "build-pip.nix")


def build_wheel(target_directory: str, requirement: str) -> str:
    package_directory = os.path.join(ROOT, "unittests", "data")
    escaped_requirement = shlex.quote(requirement)
    target_directory = os.path.abspath(target_directory)
    with tempfile.TemporaryDirectory() as build_directory:
        os.chdir(build_directory)
        logger = StreamLogger(sys.stdout)
        nix = Nix(logger=logger)
        nix.shell(
            command=f"pip wheel {escaped_requirement} --find-links {package_directory}",
            derivation_path=DERIVATION_PATH,
            nix_arguments=dict(),
        )
        for path in os.listdir("."):
            if path.endswith(".whl"):
                wheel_path = path
                break
        else:
            raise Exception("Build process did not produce .whl file")
        target_file_name = os.path.basename(wheel_path)
        target_path = os.path.join(target_directory, target_file_name)
        shutil.move(wheel_path, target_path)
    return target_file_name
