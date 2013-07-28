import sys
import copy
import json
import tempfile
import xmlrpclib
from pypi2nix.buildout import run_buildout

TMPL_START = '''{ pkgs, stdenv, fetchurl, python, lowPrio, self }:

let
  inherit (self) buildPythonPackage;
in
{'''
TMPL_END = '''
}'''
TMPL_VERSION_START = '''
} // pkgs.lib.optionalAttrs (python.majorVersion == "%s") {
'''
TMPL_VERSION_END = '''
}
'''
TMPL_NIX_EXPR = '''
  "%(name)s" = buildPythonPackage {
    name = "%(name)s";
    src = fetchurl {
        url = "%(url)s";
        md5 = "%(md5)s";
    };
    propagatedBuildInputs = [ %(dependencies)s ];
    meta = {
      description = "%(description)s";
      homepage = "%(homepage)s";
      license = "%(license)s";
    };
  };
'''

DEFAULT_ENVIRONMENT = "py27"
ENVIRONMENTS = {
    u"py26": "python26Full",
    u"py27": "python27Full",
}
LIB_VERSIONS = {
    u"py26": "2.6",
    u"py27": "2.7",
}


def main():

    try:
        f = open(sys.argv[1])
        specifications = json.load(f)
    except ValueError as e:
        raise ValueError("File %s is not valid JSON file." % sys.argv[1])
    except Exception as e:
        raise e
    finally:
        f.close()

    #eggsdir = tempfile.mkdtemp(suffix='pypi2nix-eggs')
    eggsdir = '/home/rok/.buildout/eggs'

    configs = []
    for spec in specifications:
        if isinstance(spec, basestring):
            spec = {'name': spec,
                    'environment': DEFAULT_ENVIRONMENT
                    }
        spec.setdefault('buildInputs', [])
        if 'environments' in spec:
            for environment in spec['environments']:
                temp_spec = copy.deepcopy(spec)
                temp_spec['environment'] = environment
                temp_spec['buildInputs'].append(ENVIRONMENTS[environment])
                configs.append((LIB_VERSIONS[environment], temp_spec))
        else:
            spec['buildInputs'].append(ENVIRONMENTS[DEFAULT_ENVIRONMENT])
            spec['environment'] = DEFAULT_ENVIRONMENT
            configs.append((LIB_VERSIONS[DEFAULT_ENVIRONMENT], spec))

    packages = {}
    packages_per_version = {}
    for lib_version, config in configs:
        tmp = run_buildout(eggsdir, config)
        packages_per_version.setdefault(lib_version, set([]))
        packages_per_version[lib_version] = \
            packages_per_version[lib_version].union(
                set([i for i in tmp.keys()]))
        packages.update(tmp)

    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    for package_name in packages:
        metadata = client.release_data(
            packages[package_name]['name'],
            packages[package_name]['version'])
        packages[package_name]['description'] = metadata['summary']
        packages[package_name]['homepage'] = metadata['home_page']
        packages[package_name]['license'] = metadata['license']

        release = None
        releases = client.release_urls(
            packages[package_name]['name'],
            packages[package_name]['version'])
        for item in releases:
            if item['packagetype'] == 'sdist' and \
               item['python_version'] == 'source':
                release = item
                break
        if release is None:
            raise("No source/sdist release version for %s!" % package_name)
        packages[package_name]['md5'] = release['md5_digest']
        packages[package_name]['url'] = release['url']

    print TMPL_START
    for version in packages_per_version:
        print TMPL_VERSION_START % version
        for package in packages_per_version[version]:
            if package.startswith('setuptools-'):
                continue
            tmp = copy.deepcopy(packages[package])
            tmp['name'] = package
            tmp['dependencies'] = ' '.join([
                i.startswith('setuptools-') \
                    and 'self.setuptools'
                    or 'self."%s"' % i
                for i in tmp['dependencies']
                if i != package
            ])
            tmp.setdefault('buildInputs', '')
            if tmp['url'].endswith('.zip'):
                tmp['buildInputs'] = 'pkgs.unzip'

            print TMPL_NIX_EXPR % tmp
        print TMPL_VERSION_END
