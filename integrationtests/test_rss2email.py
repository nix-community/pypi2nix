from unittest import TestCase

from .framework import IntegrationTest
from .framework import TestCommand


class Rss2Email(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return 'rss2email'

    def python_version(self):
        return '3.6'

    def requirements(self):
        return [
            'https://github.com/wking/rss2email/archive/master.zip#egg=rss2email',
        ]

    def executables_for_testing(self):
        return [
            TestCommand(command=['r2e', '--help']),
        ]

    def code_for_testing(self):
        return [
            'import rss2email',
        ]
