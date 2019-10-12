from .framework import IntegrationTest
from .framework import TestCommand


class Rss2EmailTestCase(IntegrationTest):
    name_of_testcase = "rss2email"
    code_for_testing = ["import rss2email"]
    requirements = [
        "https://github.com/wking/rss2email/archive/master.zip#egg=rss2email"
    ]

    def executables_for_testing(self):
        return [TestCommand(command=["r2e", "--help"])]
