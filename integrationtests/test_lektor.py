from .framework import IntegrationTest
from .framework import TestCommand


class LektorTestCase(IntegrationTest):
    name_of_testcase = "lektor"
    python_version = "python27"
    code_for_testing = ["import lektor"]
    requirements = ["Lektor"]
    external_dependencies = ["libffi", "openssl", "unzip"]

    def executables_for_testing(self):
        return [TestCommand(command=["lektor", "--help"])]
