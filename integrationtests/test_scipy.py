from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class ScipyTest(IntegrationTest):
    name_of_testcase = "scipy"
    code_for_testing = ["import scipy"]
    requirements = ["scipy", "numpy"]

    def external_dependencies(self):
        return ["gfortran", "blas"]

    def setup_requires(self):
        return ["numpy"]
