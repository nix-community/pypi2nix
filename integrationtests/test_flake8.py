from unittest import TestCase

from .framework import IntegrationTest


class Flake8Test(IntegrationTest, TestCase):
    name_of_testcase = "flake8"
    code_for_testing = ["import flake8"]
    requirements = ["flake8 == 3.7.7"]

    def setup_requires(self):
        return ["intreehooks", "pytest-runner", "setuptools-scm", "flit"]
