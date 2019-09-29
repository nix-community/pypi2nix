from .framework import IntegrationTest
from .framework import TestCommand


class AwscliAndRequestsTestCase(IntegrationTest):
    name_of_testcase = "awscli_and_requests"
    requirements = ["awscli", "requests"]
    python_version = "python27"
    code_for_testing = ["import awscli", "import requests"]

    def executables_for_testing(self):
        return [TestCommand(command=["aws", "help"], env={"PAGER": "none"})]
