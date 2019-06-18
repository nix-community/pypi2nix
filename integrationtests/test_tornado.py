from unittest import TestCase

from .framework import IntegrationTest


REVISION = '69253c820df473407c562a227d0ba36df25018ab'

class TornadoTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return 'tornado'

    def python_version(self):
        return '2.7'

    def requirements(self):
        return [
            '-e git+git://github.com/tornadoweb/tornado.git@69253c820df473407c562a227d0ba36df25018ab#egg=tornado',
        ]

    def code_for_testing(self):
        return [
            'import tornado'
        ]

    def requirements_file_check(self, content):
        self.assertIn(REVISION, content)

    
