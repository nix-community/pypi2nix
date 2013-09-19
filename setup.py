# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages


setup(
    name="pypi2nix",
    version="0.0.1",
    author=u"Rok Garbas, Cillian de Róiste",
    description=(
        "Scripts and tools to help create nix package expressions for "
        "python projects"
    ),
    license="GPL",
    keywords="nixos nix packaging",
    url="http://nixos.org",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    entry_points = {
        'console_scripts': [
            'pypi2nix= pypi2nix.cli:main',
        ],
    },
    packages = find_packages(),
)
