from .framework import IntegrationTest


class AiohttpTestCase(IntegrationTest):
    name_of_testcase = "aiohttp"
    code_for_testing = ["import aiohttp"]
    requirements = ["aiohttp==2.0.6.post1"]
    python_version = "python35"
