from .framework import IntegrationTest


class EmpyTestCase(IntegrationTest):
    name_of_testcase = "empy"
    code_for_testing = ["import em"]
    requirements = ["empy"]
