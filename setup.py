# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

with open('src/pypi2nix/VERSION') as f:
    version = f.read().strip()

setup(
    name="pypi2nix",
    version=version,
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
    packages = ['pypi2nix'],
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires = [
        'click',
        'requests',
    ]
)
