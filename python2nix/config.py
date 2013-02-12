"""Shared configuration options, variable etc.

This is the place to keep track of particular packages which need
special handling."""


METADATA_MAP = {
    "Home-page": "homepage",
    "License": "license",
    "Summary": "description",
}

PRE_TMPL = """
{ pkgs, python, buildPythonPackage }:

let plone42Packages = python.modules // rec {
  inherit python;
  inherit (pkgs) fetchurl stdenv;

"""

TMPL = """
  %(nixname)s = buildPythonPackage rec {
    name = "%(name)s";

    src = fetchurl {
      url = "%(url)s";
      %(hashname)s = "%(hashval)s";
    };
%(install_command)s%(build_inputs)s%(propagated_build_inputs)s
    doCheck = false;

    meta = {
%(metadata)s
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };
"""

POST_TMPL = """
  eggtestinfo = buildPythonPackage rec {
    name = "eggtestinfo-0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/e/eggtestinfo/${name}.tar.gz";
      md5 = "6f0507aee05f00c640c0d64b5073f840";
    };

    # circular dependencies
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';

    doCheck = false;

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];

    };
  };

}; in plone42Packages
"""


# These cannot be installed without some requirements
HARD_REQUIREMENTS = {
    'products_cmfactionicons': 'eggtestinfo',
    'products_cmfcalendar': 'eggtestinfo',
    'products_cmfdefault': 'eggtestinfo',
    'products_cmfuid': 'eggtestinfo',
    'products_dcworkflow': 'eggtestinfo',
    'products_cmftopic': 'eggtestinfo',
    'pastescript': 'paste pastedeploy',
}

# don't package stuff we can use from the system python packages
SYSTEM_PACKAGES = [
    'distribute',
    'lxml',
    'setuptools',
    'zc_buildout',
]

# The permissions for the skel dirs is changed by nix, which prevents
# the instance from being installed, let's skip it
IGNORE_PACKAGES = ['plone_recipe_zope2instance',]

INSTALL_COMMAND = """
    # ignore dependencies
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
"""


