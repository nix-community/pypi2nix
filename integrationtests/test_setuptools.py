from .framework import IntegrationTest


class SetuptoolsTestCase(IntegrationTest):
    name_of_testcase = "setuptools"
    code_to_test = ["import setuptools"]
    requirements = ["setuptools"]

    def requirements_file_check(self, content):
        self.assertIn('"setuptools" =', content)
