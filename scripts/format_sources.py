#!/usr/bin/env python

import os.path
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


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
    absolute_paths = [os.path.join(ROOT, relative) for relative in relative_paths]
    subprocess.run(["isort", "-rc"] + absolute_paths, check=True)
    subprocess.run(["black"] + absolute_paths, check=True)
    subprocess.run(["flake8"] + absolute_paths, check=True)
    subprocess.run(["mypy", "src"], check=True)
    subprocess.run(
        ["mypy", "--allow-untyped-defs", "--ignore-missing-imports"] + absolute_paths,
        check=True,
    )


if __name__ == "__main__":
    main()
