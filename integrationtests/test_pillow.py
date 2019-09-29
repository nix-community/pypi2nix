from .framework import IntegrationTest


class PillowTest(IntegrationTest):
    name_of_testcase = "pillow"
    code_for_testing = ["import PIL"]
    requirements = ["Pillow"]

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
