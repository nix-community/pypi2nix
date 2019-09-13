from unittest import TestCase

from .framework import IntegrationTest


class PillowTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "pillow"

    def requirements(self):
        return ["Pillow"]

    def python_version(self):
        return "python35"

    def code_for_testing(self):
        return ["import PIL"]

    def external_dependencies(self):
        return [
            "pkgconfig",
            "zlib",
            "libjpeg",
            "openjpeg",
            "libtiff",
            "freetype",
            "lcms2",
            "libwebp",
            "tcl",
        ]
