from unittest import TestCase
from unittest import expectedFailure

from .framework import IntegrationTest


class Flake8Test(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return 'flake8'

    def requirements(self):
        return [
            'flake8',
        ]

    def python_version(self):
        return '3.5'

    def code_for_testing(self):
        return ['import flake8']

    def setup_requires(self):
        return [
            'intreehooks',
            'pytest-runner',
            'setuptools-scm',
            'flit',
        ]
