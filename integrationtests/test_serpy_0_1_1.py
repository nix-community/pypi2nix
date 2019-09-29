from unittest import TestCase

from .framework import IntegrationTest


class SerpyTest(IntegrationTest, TestCase):
    name_of_testcase = "serpy"
    requirements = ["serpy==0.1.1"]

    def setup_requires(self):
        return ["six==1.12.0"]
