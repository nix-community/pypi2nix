#!/usr/bin/env python


import os
import os.path

from build_wheel import build_wheel as _build_wheel
from pypi2nix.wheels import INDEX
from repository import ROOT

TARGET_DIRECTORY = os.path.join(ROOT, "src", "pypi2nix", "wheels")
INDEX_PATH = os.path.join(TARGET_DIRECTORY, "index.json")


def build_wheel(requirement: str) -> str:
    return _build_wheel(
        TARGET_DIRECTORY,
        requirement,
    )


def main():
    requirements = [
        ('pip', 'pip>=19.3.1'),
        ('setuptools', 'setuptools'),
        ('wheel', 'wheel'),
    ]
    for name, requirement in requirements:
        file_name = build_wheel(requirement)
        INDEX[name] = file_name


if __name__ == "__main__":
    main()
