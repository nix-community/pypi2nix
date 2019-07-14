from unittest import TestCase

from .framework import IntegrationTest
from .framework import TestCommand


class AwscliAndRequestsTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "awscli_and_requests"

    def requirements(self):
        return ["awscli", "requests"]

    def python_version(self):
        return "2.7"

    def code_for_testing(self):
        return ["import awscli", "import requests"]

    def executables_for_testing(self):
        return [TestCommand(command=["aws", "help"], env={"PAGER": "none"})]
