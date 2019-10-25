#!/usr/bin/env python
"This script prepares the test fixtures for the unittests of this package"

import os
import os.path
import shutil
import subprocess

from build_wheel import build_wheel
from repository import ROOT

wheel_target_directory = os.path.join(ROOT, "unittests", "data")
TEST_PACKAGES = ["setupcfg-package", "package1", "package2", "package3", "package4"]


def build_test_package(package_name):
    package_name_with_underscores = package_name.replace("-", "_")
    package_dir = os.path.join(ROOT, "unittests", "data", package_name)
    paths_to_delete = [
        f"{package_name_with_underscores}.egg-info",
        "dist",
        f"{package_name}.tar.gz",
    ]
    for path in paths_to_delete:
        shutil.rmtree(os.path.join(package_dir, "path"), ignore_errors=True)
    subprocess.run(["python", "setup.py", "sdist"], cwd=package_dir, check=True)
    shutil.copy(
        os.path.join(package_dir, "dist", f"{package_name}-1.0.tar.gz"),
        wheel_target_directory,
    )
    shutil.move(
        os.path.join(package_dir, "dist", f"{package_name}-1.0.tar.gz"),
        os.path.join(package_dir, f"{package_name}.tar.gz"),
    )
    build_wheel(wheel_target_directory, package_dir)


def download_flit_wheel():
    build_wheel(wheel_target_directory, "flit==1.3")


if __name__ == "__main__":
    for test_package in TEST_PACKAGES:
        build_test_package(test_package)
    download_flit_wheel()
