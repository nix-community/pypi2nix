from unittest import TestCase

from .framework import IntegrationTest


class Flake8Test(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "flake8"

    def requirements(self):
        return ["flake8 == 3.7.7"]

    def python_version(self):
        return "python35"

    def code_for_testing(self):
        return ["import flake8"]

    def setup_requires(self):
        return ["intreehooks", "pytest-runner", "setuptools-scm", "flit"]
