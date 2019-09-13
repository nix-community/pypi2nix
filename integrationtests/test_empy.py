from unittest import TestCase

from .framework import IntegrationTest


class EmpyTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "empy"

    def requirements(self):
        return ["empy"]

    def python_version(self):
        return "python3"

    def code_for_testing(self):
        return ["import em"]
