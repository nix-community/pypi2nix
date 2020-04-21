from .framework import IntegrationTest


class RelativePathsTestCase(IntegrationTest):
    name_of_testcase = "relative_paths"
    requirements = ["test_package/.#egg=test_package"]

    def requirements_file_check(self, content):
        self.assertIn("src = test_package/.", content)


class RelativePathsTestCase2(IntegrationTest):
    name_of_testcase = "relative_paths_2"
    requirements = ["file://./test_package/.#egg=test_package"]

    def requirements_file_check(self, content):
        self.assertIn("src = test_package/.", content)


class RelativePathsTestCase3(IntegrationTest):
    name_of_testcase = "relative_paths_3"
    requirements = ["file://test_package/.#egg=test_package"]

    def requirements_file_check(self, content):
        self.assertIn("src = test_package/.", content)
