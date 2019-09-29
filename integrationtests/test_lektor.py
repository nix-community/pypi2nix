from .framework import IntegrationTest
from .framework import TestCommand


class LektorTest(IntegrationTest):
    name_of_testcase = "lektor"
    python_version = "python27"
    code_for_testing = ["import lektor"]
    requirements = ["Lektor"]

    def executables_for_testing(self):
        return [TestCommand(command=["lektor", "--help"])]

    def external_dependencies(self):
        return ["libffi", "openssl", "unzip"]
