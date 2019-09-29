from .framework import IntegrationTest


class ConnexionTestCase(IntegrationTest):
    name_of_testcase = "connexion"
    requirements = ["connexion"]
    code_for_testing = ["import connexion"]
    constraints = ["clickclick == 1.2.1", "flake8 == 3.7.7"]

    def setup_requires(self):
        return ["flit", "pytest-runner", "setuptools-scm", "vcversioner", "flake8"]
