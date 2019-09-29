from unittest import TestCase
from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class LdapTest(IntegrationTest, TestCase):
    name_of_testcase = "ldap"
    python_version = "python27"
    code_for_testing = ["import ldap"]
    requirements = ["python-ldap"]

    def extra_environment(self):
        return {
            "NIX_CFLAGS_COMPILE": '"-I${pkgs.cyrus_sasl.dev}/include/sasl $NIX_CFLAGS_COMPILE"'
        }

    def external_dependencies(self):
        return ["openldap", "cyrus_sasl", "openssl"]
