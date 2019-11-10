# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    use_scm_version={
        "write_to": "src/pypi2nix/_version.py",
        "write_to_template": 'pypi2nix_version = "{version}"\n',
    }
)
