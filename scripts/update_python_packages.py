#!/usr/bin/env python

import sys

from pypi2nix.logger import StreamLogger
from pypi2nix.pypi import Pypi
from pypi2nix.utils import prefetch_git
from pypi2nix.wheels import Index


def main():
    logger = StreamLogger(sys.stdout)
    pypi = Pypi(logger=logger)
    pip_requirements = ["setuptools", "wheel"]
    git_requirements = [("pip", "https://github.com/pypa/pip.git")]
    index = Index(logger=logger)
    for name in pip_requirements:
        insert_pip_requirement(index, name, logger, pypi)
    for name, url in git_requirements:
        insert_git_requirement(index, name, url)
    assert index.is_valid()


def insert_pip_requirement(index, requirement, logger, pypi):
    package = pypi.get_package(requirement)
    source_release = pypi.get_source_release(name=requirement, version=package.version)
    if source_release is None:
        logger.warning(f"Could not update source for package `{requirement}`")
        return
    index[requirement] = index.UrlEntry(
        url=source_release.url, sha256=source_release.sha256_digest
    )


def insert_git_requirement(index, name, url):
    repo_data = prefetch_git(url)
    index[name] = index.GitEntry(
        url=repo_data["url"], rev=repo_data["rev"], sha256=repo_data["sha256"],
    )


if __name__ == "__main__":
    main()
