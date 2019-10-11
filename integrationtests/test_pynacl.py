from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class PynaclTestCase(IntegrationTest):
    name_of_testcase = "pynacl"
    requirements = ["pynacl"]
    external_dependencies = ["libffi"]
    explicit_build_directory = True
