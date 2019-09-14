#!/usr/bin/env python
"This script prepares the test fixtures for the unittests of this package"

import os.path
import shutil
import subprocess

from build_wheel import build_wheel
from repository import ROOT


def package_setupcfg_package():
    package_dir = os.path.join(ROOT, "unittests", "data", "setupcfg-package")
    paths_to_delete = ["setupcfg_package.egg-info", "dist", "setupcfg-package.tar.gz"]
    for path in paths_to_delete:
        shutil.rmtree(os.path.join(package_dir, "path"), ignore_errors=True)
    subprocess.run(["python", "setup.py", "sdist"], cwd=package_dir, check=True)
    shutil.move(
        os.path.join(package_dir, "dist", "setupcfg-package-1.0.tar.gz"),
        os.path.join(package_dir, "setupcfg-package.tar.gz"),
    )
    wheel_target_directory = os.path.join(ROOT, "unittests", "data")
    build_wheel(wheel_target_directory, package_dir)


if __name__ == "__main__":
    package_setupcfg_package()
