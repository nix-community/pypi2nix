from unittest import TestCase
from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class ScipyTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "scipy"

    def requirements(self):
        return ["scipy", "numpy"]

    def python_version(self):
        return "python3"

    def external_dependencies(self):
        return ["gfortran", "blas"]

    def setup_requires(self):
        return ["numpy"]

    def code_for_testing(self):
        return ["import scipy"]
