from .framework import IntegrationTest


class FavaTestCase(IntegrationTest):
    name_of_testcase = "fava"
    requirements = ["fava==1.13"]
    external_dependencies = ["libxml2", "libxslt"]
    constraints = ["jaraco-functools == 2.0"]
