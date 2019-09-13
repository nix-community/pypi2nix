from unittest import TestCase

from .framework import IntegrationTest


class Aiohttp(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return "aiohttp"

    def requirements(self):
        return ["aiohttp==2.0.6.post1"]

    def python_version(self):
        return "python35"

    def code_for_testing(self):
        return ["import aiohttp"]
