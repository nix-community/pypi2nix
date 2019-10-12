from unittest import expectedFailure

from .framework import IntegrationTest


@expectedFailure
class LdapTestCase(IntegrationTest):
    name_of_testcase = "ldap"
    python_version = "python27"
    code_for_testing = ["import ldap"]
    requirements = ["python-ldap"]
    external_dependencies = ["openldap", "cyrus_sasl", "openssl"]

    def extra_environment(self):
        return {
            "NIX_CFLAGS_COMPILE": '"-I${pkgs.cyrus_sasl.dev}/include/sasl $NIX_CFLAGS_COMPILE"'
        }
