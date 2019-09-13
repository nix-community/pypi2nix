from unittest import TestCase

from .framework import IntegrationTest
from .framework import TestCommand


class LektorTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "lektor"

    def requirements(self):
        return ["Lektor"]

    def python_version(self):
        return "python27"

    def code_for_testing(self):
        return ["import lektor"]

    def executables_for_testing(self):
        return [TestCommand(command=["lektor", "--help"])]

    def external_dependencies(self):
        return ["libffi", "openssl", "unzip"]
