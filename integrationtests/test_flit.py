from unittest import TestCase

from .framework import IntegrationTest


class FlitTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "flit"

    def python_version(self):
        return "3.5"

    def requirements(self):
        return ["flit"]

    def setup_requires(self):
        return ["intreehooks"]
