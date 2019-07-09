from unittest import TestCase

from .framework import IntegrationTest

REVISION = "a209fb6"


class Flake8MercurialTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "flake8-mercurial"

    def python_version(self):
        return "3"

    def requirements(self):
        return [
            "-e hg+https://bitbucket.org/tarek/flake8@{revision}#egg=flake8".format(
                revision=REVISION
            ),
            "pep8",
        ]

    def setup_requires(self):
        return ["setuptools-scm", "pytest-runner"]

    def code_for_testing(self):
        return ["import flake8"]

    def requirements_file_check(self, content):
        self.assertIn(REVISION, content)
