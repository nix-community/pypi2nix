#!/usr/bin/env python

import sys

from pypi2nix.logger import StreamLogger
from pypi2nix.pypi import Pypi
from pypi2nix.wheels import INDEX


def main():
    logger = StreamLogger(sys.stdout)
    pypi = Pypi(logger=logger)
    requirements = ["pip", "setuptools", "wheel"]
    for name in requirements:
        package = pypi.get_package(name)
        source_release = pypi.get_source_release(name=name, version=package.version)
        if source_release is None:
            logger.warning(f"Could not update source for package `{name}`")
            continue
        INDEX[name] = INDEX.Entry(
            url=source_release.url, sha256=source_release.sha256_digest
        )


if __name__ == "__main__":
    main()
