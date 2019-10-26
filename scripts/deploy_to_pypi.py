#!/usr/bin/env python
import os
import argparse
import subprocess

from pypi2nix.version import pypi2nix_version


def set_up_environment():
    os.putenv("SOURCE_DATE_EPOCH", "315532800")


def parse_args():
    parser = argparse.ArgumentParser(description="Deploy pypi2nix to pypi")
    parser.add_argument("--production", action="store_true", default=False)
    return parser.parse_args()


def get_pypi_name_from_args(args):
    return "pypi" if args.production else "test-pypi"


def deploy_to(pypi_name):
    subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
    distribution_paths = [
        f"dist/pypi2nix-{pypi2nix_version}.tar.gz",
        f"dist/pypi2nix-{pypi2nix_version}-py3-none-any.whl",
    ]
    subprocess.run(
        ["twine", "upload", "-r", pypi_name] + distribution_paths, check=True
    )


def main():
    set_up_environment()
    args = parse_args()
    pypi_name = get_pypi_name_from_args(args)
    deploy_to(pypi_name)


if __name__ == "__main__":
    main()
