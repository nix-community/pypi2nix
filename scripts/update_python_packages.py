#!/usr/bin/env python

import sys

from package_source import PackageSource
from pypi2nix.logger import StreamLogger
from pypi2nix.pypi import Pypi
from pypi2nix.wheels import Index


def main():
    logger = StreamLogger(sys.stdout)
    pypi = Pypi(logger=logger)
    pip_requirements = ["setuptools", "wheel"]
    git_requirements = ["pip"]
    index = Index(logger=logger)
    package_source = PackageSource(index=index, pypi=pypi, logger=logger)
    for requirement in pip_requirements:
        package_source.update_package_from_pip(requirement)
    for requirement in git_requirements:
        package_source.update_package_from_master(requirement)


if __name__ == "__main__":
    main()
