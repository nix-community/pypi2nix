#!/usr/bin/env python

import os
import os.path
import subprocess
from typing import List

from repository import ROOT


def main():
    relative_paths = [
        "src",
        "unittests",
        "integrationtests",
        "conftest.py",
        "setup.py",
        "mypy",
        "scripts",
    ]
    integration_test_nix_files = find_nix_files_in_integration_tests()
    absolute_paths = [os.path.join(ROOT, relative) for relative in relative_paths]
    subprocess.run(
        ["nixfmt", "default.nix", "src/pypi2nix/pip/bootstrap.nix"]
        + integration_test_nix_files,
        check=True,
    )
    subprocess.run(["isort", "-rc"] + absolute_paths, check=True)
    subprocess.run(["black"] + absolute_paths, check=True)
    subprocess.run(["flake8"] + absolute_paths, check=True)
    subprocess.run(["mypy", "src"], check=True)
    subprocess.run(
        ["mypy", "--allow-untyped-defs", "--ignore-missing-imports"] + absolute_paths,
        check=True,
    )


def find_nix_files_in_integration_tests() -> List[str]:
    found_files: List[str] = []
    for root, _, files in os.walk("integrationtests"):
        found_files += [
            os.path.join(root, file) for file in files if file.endswith(".nix")
        ]
    return found_files


if __name__ == "__main__":
    main()
