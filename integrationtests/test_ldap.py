from unittest import TestCase
from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class LdapTest(IntegrationTest, TestCase):
    def name_of_testcase(self):
        return 'ldap'

    def requirements(self):
        return [
            'python-ldap',
        ]

    def python_version(self):
        return '2.7'

    def code_for_testing(self):
        return ['import ldap']

    def extra_environment(self):
        return {
            "NIX_CFLAGS_COMPILE": '"-I${pkgs.cyrus_sasl.dev}/include/sasl $NIX_CFLAGS_COMPILE"',
        }

    def external_dependencies(self):
        return [
            'openldap',
            'cyrus_sasl',
            'openssl',
        ]
