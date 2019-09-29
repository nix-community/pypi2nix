from .framework import IntegrationTest

REVISION = "69253c820df473407c562a227d0ba36df25018ab"


class TornadoTestCase(IntegrationTest):
    name_of_testcase = "tornado"
    code_for_testing = ["import tornado"]
    python_version = "python27"
    requirements = [
        "-e git+git://github.com/tornadoweb/tornado.git@69253c820df473407c562a227d0ba36df25018ab#egg=tornado"
    ]

    def requirements_file_check(self, content):
        self.assertIn(REVISION, content)
