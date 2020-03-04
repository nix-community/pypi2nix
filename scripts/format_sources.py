#!/usr/bin/env python

import os
import os.path
import subprocess
import sys
from typing import List

from pypi2nix.logger import Logger
from pypi2nix.logger import StreamLogger
from repository import ROOT


def main():
    logger: Logger = initialize_logger()
    relative_paths = [
        "src",
        "unittests",
        "integrationtests",
        "conftest.py",
        "setup.py",
        "mypy",
        "scripts",
    ]
    format_nix_files(logger=logger)
    absolute_paths = [os.path.join(ROOT, relative) for relative in relative_paths]
    subprocess.run(["isort", "-rc"] + absolute_paths, check=True)
    subprocess.run(["black"] + absolute_paths, check=True)
    subprocess.run(["flake8"] + absolute_paths, check=True)
    subprocess.run(["mypy", "src"], check=True)
    subprocess.run(
        ["mypy", "--allow-untyped-defs", "--ignore-missing-imports"] + absolute_paths,
        check=True,
    )


def format_nix_files(logger: Logger) -> None:
    if is_nixfmt_installed():
        logger.info("Formatting nix files")
        integration_test_nix_files = find_nix_files_in_integration_tests()
        subprocess.run(
            ["nixfmt", "default.nix", "src/pypi2nix/pip/bootstrap.nix"]
            + integration_test_nix_files,
            check=True,
        )
    else:
        logger.warning("Could not find `nixfmt` executable.  Cannot format .nix files")


def find_nix_files_in_integration_tests() -> List[str]:
    found_files: List[str] = []
    for root, _, files in os.walk("integrationtests"):
        found_files += [
            os.path.join(root, file) for file in files if file.endswith(".nix")
        ]
    return found_files


def initialize_logger() -> Logger:
    return StreamLogger(output=sys.stdout)


def is_nixfmt_installed() -> bool:
    process_result = subprocess.run("nixfmt --version", shell=True, capture_output=True)
    return process_result.returncode == 0


if __name__ == "__main__":
    main()
