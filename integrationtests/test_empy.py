from .framework import IntegrationTest


class EmpyTest(IntegrationTest):
    name_of_testcase = "empy"
    code_for_testing = ["import em"]
    requirements = ["empy"]
