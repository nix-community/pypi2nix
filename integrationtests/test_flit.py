from unittest import TestCase

from .framework import IntegrationTest


class FlitTest(IntegrationTest, TestCase):
    name_of_testcase = "flit"
    requirements = ["flit"]
