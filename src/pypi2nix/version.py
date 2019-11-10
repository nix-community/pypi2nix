try:
    from ._version import pypi2nix_version
except ImportError:
    from setuptools_scm import get_version

    pypi2nix_version = get_version()
