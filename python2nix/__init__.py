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
    """
    """

    def __init__(self, dists, ignores, extends):
        self.ignores = ignores
        self.extends = extends

        if self.extends and os.path.exists(self.extends):
            fd = open(extends)
            self.extends = json.load(fd)
            fd.close()

        self.dist = None
        self.dists = {}
        for dist_name in dists:
            dist = distlib.locators.locate(dist_name, True)
            if self.dist is None:
                self.dist = dist
            self.process(dist)

    def process(self, dist):
        nixname = dist.name.replace('.', '_').replace('-', '_').lower()
        if nixname in self.dists:
            return nixname

        deps = []
        for dep_name in dist.requires:
            print dep_name
            dep_dist = distlib.locators.locate(dep_name, True)
            deps.append(self.process(dep_dist))

        buildtime_deps = []
        if dist.download_url.endswith('.zip'):
            buildtime_deps.append('pkgs.unzip')

        self.dists[nixname] = {
            'nixname': nixname,
            'name': dist.name,
            'version': dist.version,
            'download_url': dist.download_url,
            'md5sum': dist.md5_digest,
            'deps': ' '.join(deps),
            'buildtime_deps': ' '.join(buildtime_deps),
        }
        return nixname

    def to_string(self):
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

    def to_file(self, filename):
        f = open(filename, 'w+')
        try:
            f.write(self.to_string())
        finally:
            f.close()
        return 'Nix expressions for "%s" distribution written to: %s' % (
            self.dist.name, filename)
