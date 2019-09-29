from .framework import IntegrationTest


class PynaclTestCase(IntegrationTest):
    name_of_testcase = "pynacl"
    requirements = ["pynacl"]
    external_dependencies = ['libffi']
    explicit_build_directory = True
