from unittest import TestCase

from .framework import IntegrationTest


class LocalPathTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "local_path"

    def python_version(self):
        return "python3"

    def requirements(self):
        return ["-e egg#egg=local_path"]
