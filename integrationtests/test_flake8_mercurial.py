from .framework import IntegrationTest

REVISION = "a209fb6"


class Flake8MercurialTestCase(IntegrationTest):
    name_of_testcase = "flake8-mercurial"
    code_for_testing = ["import flake8"]
    requirements = [
        "-e hg+https://bitbucket.org/tarek/flake8@{revision}#egg=flake8".format(
            revision=REVISION
        )
    ]

    def setup_requires(self):
        return ["setuptools-scm", "pytest-runner"]

    def requirements_file_check(self, content):
        self.assertIn(REVISION, content)
