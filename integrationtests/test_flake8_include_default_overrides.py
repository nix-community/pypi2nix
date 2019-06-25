from unittest import TestCase

from .framework import IntegrationTest


class Flake8IncludeDefaultOverrides(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return 'flake8_include_default_overrides'

    def requirements(self):
        return [
            'flake8'
        ]

    def setup_requires(self):
        return [
            'setuptools-scm',
            'pytest-runner',
            'flit',
            'intreehooks',
        ]

    def code_for_testing(self):
        return [
            'import flake8',
        ]

    def python_version(self):
        return '3.5'

    default_overrides = True
