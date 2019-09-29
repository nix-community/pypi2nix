from unittest import TestCase

from .framework import IntegrationTest


class EmpyTest(IntegrationTest, TestCase):
    name_of_testcase = "empy"
    code_for_testing = ["import em"]
    requirements = ["empy"]
