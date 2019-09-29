from unittest import TestCase

from .framework import IntegrationTest


class LocalPathTest(IntegrationTest, TestCase):
    name_of_testcase = "local_path"
    requirements = ["-e egg#egg=local_path"]
