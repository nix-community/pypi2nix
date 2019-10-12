from .framework import IntegrationTest


class LocalPathTestCase(IntegrationTest):
    name_of_testcase = "local_path"
    requirements = ["-e egg#egg=local_path"]
