from unittest import TestCase

from .framework import IntegrationTest


class Flake8IncludeDefaultOverrides(IntegrationTest, TestCase):
    name_of_testcase = "flake8_include_default_overrides"
    code_for_testing = ["import flake8"]
    default_overrides = True
    requirements = ["flake8"]

    def setup_requires(self):
        return ["setuptools-scm", "pytest-runner", "flit", "intreehooks"]
