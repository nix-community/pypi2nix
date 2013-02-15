# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name = "python2nix",
    version = "0.0.1",
    author = u"Rok Garbas, Cillian de Róiste",
    description = (
        "Scripts and tools to help create nix package expressions for "
        "python projects"),
    license = "GPL",
    keywords = "NixOS Nix Packaging",
    url = "http://nixos.org",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],

    install_requires=[
        'distutils2',
    ],
    entry_points = {
        'console_scripts': [
            'python2nix = python2nix.scripts:python2nix',
            'nix-list-python-packages = python2nix.scripts:nix_list_python_packages',
        ],
    }
)
