from .framework import IntegrationTest


class Aiohttp(IntegrationTest):
    name_of_testcase = "aiohttp"
    code_for_testing = ["import aiohttp"]
    requirements = ["aiohttp==2.0.6.post1"]
