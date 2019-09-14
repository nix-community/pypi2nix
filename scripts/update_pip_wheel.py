#!/usr/bin/env python


import os
import os.path

from build_wheel import build_wheel
from pypi2nix.wheels import INDEX
from repository import ROOT

TARGET_DIRECTORY = os.path.join(ROOT, "src", "pypi2nix", "wheels")
INDEX_PATH = os.path.join(TARGET_DIRECTORY, "index.json")


def build_pip_wheel(target_directory: str) -> str:
    return build_wheel(
        target_directory,
        "https://github.com/seppeljordan/pip/archive/issue-6222.tar.gz",
    )


def main():
    file_name = build_pip_wheel(TARGET_DIRECTORY)
    INDEX["pip"] = file_name


if __name__ == "__main__":
    main()
