import json
from distutils2.pypi import xmlrpc
from distutils2.version import get_version_predicate

TMPL_TOP = '''{ pkgs, stdenv, fetchurl, python, lowPrio, self }:

let
  inherit (self) buildPythonPackage;

in
{'''
TMPL_BOTTOM = '''
}
'''
TMPL_EXPR = '''
  {
    name = "%(name)s";
  }
'''


class PypiPackage(object):

    def __init__(self, name, version=None):
        self.name = name
        self.version = version
        self.pypi = xmlrpc.Client()

    def __str__(self):
        if self.version is None:
            releases = self.pypi.get_releases(
                self.name, show_hidden=True, force_update=True)
            predicate = get_version_predicate(self.name)
            self.version = str(releases.get_last(predicate).version)

        release = self.pypi.get_distributions(self.name, self.version)
        print release.dists['sdist']

        import pdb; pdb.set_trace()

        return TMPL_EXPR % dict(name=self.name)


def fetch_package(self, config):
    if isinstance(config, basestring):
        name = config
        requirements = {}
    else:
        name = config['name']
        requirements = config['requirements']

    version = None
    if name in requirements:
        version = requirements[name]

    if name not in self.cache or version not in self.cache[name]:
        self.cache.setdefault(name, {})
        self.cache[name][version] = PypiPackage(name, version)

        # TODO: handle dependencies here

    return self.cache[name][version]


def lalala(x):
    print 'aaaa'
    return x
