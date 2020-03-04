from .framework import IntegrationTest


class AppDirsTestCase(IntegrationTest):
    """This test checks if we handle quote characters '"' in package descriptions.

    The appdirs package has a description that includes a '"'.  This
    description gets rendered into the "meta" attribute of the result
    nix derivation.  We evaluate this attribute to make sure that
    everything is escaped fine.
    """

    name_of_testcase = "appdirs"
    requirements = ["appdirs==1.4.3"]
    additional_paths_to_build = ["packages.appdirs.meta"]
