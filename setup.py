# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name="pypi2nix",
    version=open("VERSION").read(),
    author=u"Rok Garbas, Cillian de Róiste, Jaka Hudoklin",
    description=(
        "A tool that generates nix expressions for your python packages, so "
        "you don't have to."
    ),
    license="BSD",
    keywords="nixos nix packaging",
    url="https://github.com/NixOS/pypi2nix",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points = {
        'console_scripts': [
            'pypi2nix = pypi2nix.cli:main',
        ],
    },
    packages = find_packages(),
)
