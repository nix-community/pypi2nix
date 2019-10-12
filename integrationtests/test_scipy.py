from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class ScipyTestCase(IntegrationTest):
    name_of_testcase = "scipy"
    code_for_testing = ["import scipy"]
    requirements = ["scipy", "numpy"]
    external_dependencies = ["gfortran", "blas"]

    def setup_requires(self):
        return ["numpy"]
