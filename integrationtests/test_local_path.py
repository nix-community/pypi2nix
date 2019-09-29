from .framework import IntegrationTest


class LocalPathTest(IntegrationTest):
    name_of_testcase = "local_path"
    requirements = ["-e egg#egg=local_path"]
