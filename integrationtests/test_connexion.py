from unittest import TestCase

from .framework import IntegrationTest


class ConnexionTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "connexion"

    def requirements(self):
        return ["connexion"]

    def python_version(self):
        return "3.7"

    def setup_requires(self):
        return [
            "flake8",
            "flit",
            "pytest-runner",
            "setuptools-scm",
            "vcversioner",
            "intreehooks",
        ]

    def code_for_testing(self):
        return ["import connexion"]
