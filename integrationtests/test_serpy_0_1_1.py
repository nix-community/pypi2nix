from unittest import TestCase

from .framework import IntegrationTest


class SerpyTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "serpy"

    def python_version(self):
        return "python3"

    def requirements(self):
        return ["serpy==0.1.1"]

    def setup_requires(self):
        return ["six==1.12.0"]
