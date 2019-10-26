#!/usr/bin/env python
import os
import os.path
import shutil
import subprocess

from pypi2nix.version import pypi2nix_version


def set_up_environment():
    os.putenv("SOURCE_DATE_EPOCH", "315532800")
    os.unsetenv("PYTHONPATH")


def create_sdist():
    shutil.rmtree(os.path.join("src", "pypi2nix.egg-info"), ignore_errors=True)
    subprocess.run(["build/venv/bin/python", "setup.py", "sdist"], check=True)


def create_virtual_env():
    os.makedirs("build", exist_ok=True)
    try:
        shutil.rmtree("build/venv")
    except FileNotFoundError:
        pass
    subprocess.run(["python", "-m", "venv", "build/venv"], check=True)


def create_wheel():
    shutil.rmtree(os.path.join("src", "pypi2nix.egg-info"), ignore_errors=True)
    subprocess.run(["build/venv/bin/pip", "install", "wheel"], check=True)
    subprocess.run(["build/venv/bin/python", "setup.py", "bdist_wheel"], check=True)


def install_sdist():
    subprocess.run(
        ["build/venv/bin/pip", "install", f"dist/pypi2nix-{pypi2nix_version}.tar.gz"],
        check=True,
    )


def install_wheel():
    subprocess.run(
        [
            "build/venv/bin/pip",
            "install",
            f"dist/pypi2nix-{pypi2nix_version}-py3-none-any.whl",
        ],
        check=True,
    )


def run_help_command():
    subprocess.run(["build/venv/bin/pypi2nix", "--help"], check=True)


def main():
    set_up_environment()
    create_virtual_env()
    create_sdist()
    install_sdist()
    run_help_command()
    create_virtual_env()
    create_wheel()
    install_wheel()
    run_help_command()


if __name__ == "__main__":
    main()
