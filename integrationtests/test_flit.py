from unittest import TestCase

from .framework import IntegrationTest


class FlitTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "flit"

    def python_version(self):
        return "python35"

    def requirements(self):
        return ["flit"]
