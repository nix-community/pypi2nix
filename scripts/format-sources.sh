#!/usr/bin/env sh

set -e
set -x

PYTHON_SOURCES="src/ unittests/ integrationtests/ conftest.py setup.py mypy/ prepare-test-data.py scripts/"

isort -rc $PYTHON_SOURCES
black $PYTHON_SOURCES

flake8 $PYTHON_SOURCES --enable-extensions=U10
mypy src/pypi2nix
mypy unittests/ integrationtests/ conftest.py prepare-test-data.py scripts/ --allow-untyped-defs --ignore-missing-imports
