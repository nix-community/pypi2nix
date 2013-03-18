import os
import json
import distlib.locators


TEMPLATE = """
  %(nixname)s = buildPythonPackage rec {
    name = "%(name)s-%(version)s";
    src = fetchurl {
      url = "%(download_url)s";
      md5 = "%(md5sum)s";
    };
    buildInputs = [ %(buildtime_deps)s ];
    propagatedBuildInputs = [ %(deps)s ];
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
"""

ALL_TEMPLATE = '''{ pkgs, python, buildPythonPackage }:

let %(distname)s = python.modules // rec {
  inherit python;
  inherit (pkgs) fetchurl stdenv;
%(expressions)s
}; in %(distname)s'''


class Pypi2Nix(object):

    def __init__(self, dists, ignores, extends):
        self.ignores = ignores
        self.extends = extends

        self.dist = None
        self.dists = {}
        for dist_name in dists:
            dist = distlib.locators.locate(dist_name)
            if self.dist is None:
                self.dist = dist
            self.process(dist)

    def get_nixname(self, dist):
        name = dist.name.split(' ')[0]
        name = name.replace('.', '_').replace('-', '_')
        return name.lower()

    def process(self, dist):
        nixname = self.get_nixname(dist)
        if nixname in self.dists:
            return nixname

        buildtime_deps = []
        if dist.download_url.endswith('.zip'):
            buildtime_deps.append('pkgs.unzip')

        self.dists[nixname] = {
            'nixname': nixname,
            'name': dist.name,
            'version': dist.version,
            'download_url': dist.download_url,
            'md5sum': dist.md5_digest,
            'buildtime_deps': ' '.join(buildtime_deps),
        }

        deps = []
        for dep_name in dist.requires:
            dep_dist = distlib.locators.locate(dep_name)
            dep_nixname = self.get_nixname(dep_dist)
            if dep_nixname in self.dists:
                continue
            print dep_name
            self.process(dep_dist)
            if dep_dist.name not in self.ignores:
                deps.append(dep_nixname)

        self.dists[nixname]['deps'] = ' '.join(deps)

        return nixname

    def __str__(self):
        distname = self.dist.name + self.dist.version.replace('.', '')
        distname = distname[0].lower() + distname[1:]
        distname += 'Packages'
        if self.extends:
            self.dists.update(self.extends)
        return ALL_TEMPLATE % {
            'distname': distname,
            'expressions': ''.join([
                TEMPLATE % self.dists[nixname]
                for nixname in self.dists
                if self.dists[nixname]['name'] not in self.ignores])}
