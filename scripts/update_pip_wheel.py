#!/usr/bin/env python


import os
import os.path
import shutil
import sys
import tempfile

from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix

HERE = os.path.abspath(os.path.dirname(__file__))
DERIVATION_PATH = os.path.join(HERE, "build-pip.nix")
TARGET_PATH = os.path.join(
    os.path.dirname(HERE), "src", "pypi2nix", "wheels", "pip.whl"
)


def build_pip_wheel(target_path: str):
    with tempfile.TemporaryDirectory() as build_directory:
        os.chdir(build_directory)
        logger = StreamLogger(sys.stdout)
        nix = Nix(logger=logger)
        nix.shell(
            command="pip wheel https://github.com/seppeljordan/pip/archive/issue-6222.tar.gz",
            derivation_path=DERIVATION_PATH,
            nix_arguments=dict(),
        )
        for path in os.listdir("."):
            if path.endswith(".whl"):
                wheel_path = path
                break
        else:
            raise Exception("Build process did not produce .whl file")
        shutil.move(wheel_path, target_path)


def main():
    build_pip_wheel(TARGET_PATH)


if __name__ == "__main__":
    main()
