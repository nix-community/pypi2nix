import copy
import json
import distlib.version
import distlib.locators

#distlib.locators.default_locator.scheme = '

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
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.iElectric
      ];
      platforms = stdenv.lib.platforms.all;
    };
  };
"""

ALL_TEMPLATE = '''{ pkgs, python, pythonPackages, buildPythonPackage }:

let %(distname)s = python.modules // rec {
  inherit python;
  inherit (pythonPackages) setuptools;
  inherit (pkgs) fetchurl stdenv;
%(expressions)s
}; in %(distname)s
'''


class Pypi2Nix(object):

    def __init__(self, dists, ignores=[], extends=None, pins=None):
        self.ignores = ignores
        if extends:
            extends = json.load(extends)
        self.extends = extends
        if pins:
            pins = self.get_pins(pins)
        self.pins = pins

        self.rev_deps = {}
        self.dist = None
        self.dists = {}
        for dist_name in dists:
            if self.pins and dist_name in self.pins:
                dist_name = "%s (== %s)" % (dist_name, self.pins[dist_name])
            dist = self.locate(dist_name)
            if self.dist is None:
                self.dist = dist
            self.process(dist)

    def locate(self, name):
        print name
        try:
            dist = distlib.locators.locate(name, True)
        except distlib.version.UnsupportedVersionError:
            # default version scheme (adaptive) should also fallback to
            # legacy version scheme, doing this manually
            # needed for "pytz (==2012g)" requirement
            scheme = distlib.locators.default_locator.scheme
            distlib.locators.default_locator.scheme = 'legacy'
            dist = distlib.locators.locate(name, True)
            distlib.locators.default_locator.scheme = scheme
        return dist

    def get_pins(self, pins):
        dist_pins = {}
        for line in pins:
            if '==' not in line:
                continue
            line = line.split('==')
            if len(line) != 2:
                continue
            dist_pins[line[0]] = line[1].strip()
        return dist_pins

    def get_nixname(self, name):
        name = name.split(' ')[0]
        name = name.replace('.', '_').replace('-', '_')
        return name.lower()

    def process_dist(self, dep_name_full, rev_deps):
        dep_name = dep_name_full.split(' ')[0]
        if self.pins and dep_name in self.pins:
            dep_name = "%s (== %s)" % (dep_name, self.pins[dep_name])
        else:
            dep_name = dep_name_full

        dep_dist = self.locate(dep_name)
        dep_nixname = self.get_nixname(dep_dist.name)

        if dep_nixname not in self.dists:
            self.process(dep_dist)

        if dep_nixname not in rev_deps:
            return dep_nixname

    def process(self, dist, rev_deps=[]):
        nixname = self.get_nixname(dist.name)
        if nixname in self.dists:
            return nixname

        rev_deps.append(nixname)
        copy_rev_deps = copy.deepcopy(rev_deps)

        self.dists[nixname] = {
            'nixname': nixname,
            'name': dist.name,
            'version': dist.version,
            'download_url': dist.download_url.replace(dist.name + '-' + dist.version, '${name}'),
            'md5sum': dist.md5_digest,
        }

        buildtime_deps = []
        if dist.download_url.endswith('.zip'):
            buildtime_deps.append('pkgs.unzip')
        for dep_name in list(dist.setup_requires) + list(dist.test_requires):
            dep_nixname = self.get_nixname(dep_name)
            self.rev_deps.setdefault(dep_nixname, [])
            self.rev_deps[dep_nixname].append(nixname)
            dep_nixname = self.process_dist(dep_name, [])
            if dep_nixname:
                buildtime_deps.append(dep_nixname)

        deps = []
        for dep_name in dist.requires:
            dep_nixname = self.get_nixname(dep_name)
            self.rev_deps.setdefault(dep_nixname, [])
            self.rev_deps[dep_nixname].append(nixname)
            dep_nixname = self.process_dist(dep_name, copy_rev_deps)
            if dep_nixname:
                deps.append(dep_nixname)

        self.dists[nixname]['deps'] = ' '.join(deps)
        self.dists[nixname]['buildtime_deps'] = ' '.join(buildtime_deps)

    def __str__(self):
        distname = self.dist.name + self.dist.version.replace('.', '')
        distname = distname[0].lower() + distname[1:]
        distname += 'Packages'
        if self.extends:
            for name in self.extends:
                self.dists[name].update(self.extends[name])
        return ALL_TEMPLATE % {
            'distname': distname,
            'expressions': ''.join([
                TEMPLATE % self.dists[nixname]
                for nixname in self.dists
                if self.dists[nixname]['name'] not in self.ignores])}
