import os
import sys
import copy
import json
import errno
import xmlrpclib
from pypi2nix.buildout import run_buildout


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def deep_update(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = copy.deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = deep_update(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


TMPL_START = '''{ pkgs, stdenv, fetchurl, python, self }:

let
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
#Plone = self."Plone-4.3.1";
TMPL_NIX_EXPR = '''
  "%(name)s" = self.buildPythonPackage {
    name = "%(name)s";
    src = fetchurl {
        url = "%(url)s";
        md5 = "%(md5)s";
    };
    doCheck = %(doCheck)s;
    buildInputs = [ %(buildInputs)s ];
    propagatedBuildInputs = [ %(propagatedBuildInputs)s ];%(configurePhase)s
    installCommand = ''%(installCommand)s'';
    meta = {
      description = ''
        %(description)s
        '';
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
        print "File %s is not valid JSON file." % sys.argv[1]
        print e
        sys.exit(1)
    except Exception as e:
        print "Usage: pypi2nix <jsonfile>"
        if len(sys.argv) == 1:
            print "Please provide <jsonfile>!."
        else:
            print e
        sys.exit(1)

    f.close()

    eggsdir = os.path.expanduser('~/.buildout/eggs')
    mkdir_p(eggsdir)

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
        packages = deep_update(packages, tmp)

    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    for package_name in packages:
        try:
            metadata = client.release_data(
                packages[package_name]['name'],
                packages[package_name]['version'])
            packages[package_name]['description'] = metadata['summary']
            packages[package_name]['homepage'] = metadata['home_page']
            packages[package_name]['license'] = metadata['license']
        except:
            packages[package_name]['description'] = ""
            packages[package_name]['homepage'] = ""
            packages[package_name]['license'] = ""

        release = None
        releases = client.release_urls(
            packages[package_name]['name'].replace('webob', 'WebOb'),
            packages[package_name]['version'])
        for item in releases:
            if item['packagetype'] == 'sdist' and \
               item['python_version'] == 'source':
                release = item
                break
        if release is None:
            raise Exception("No source/sdist release version for %s!" % package_name)
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

            tmp['propagatedBuildInputs'] = ' '.join([
                i.startswith('setuptools-')
                and 'self.setuptools'
                or ((i.startswith('python.modules.') or i.startswith('pkgs.'))
                    and i or 'self."%s"' % i)
                for i in tmp['propagatedBuildInputs']
                if i != package
            ])

            tmp.setdefault('buildInputs', [])
            tmp['buildInputs'] = [
                (i.startswith('python.modules.') or i.startswith('pkgs.'))
                and i or 'self."%s"' % i
                for i in tmp['buildInputs']]
            if tmp['url'].endswith('.zip'):
                tmp['buildInputs'].append('pkgs.unzip')
            tmp['buildInputs'] = ' '.join(tmp['buildInputs'])

            if tmp['configurePhase'] is None:
                tmp['configurePhase'] = ""
            else:
                tmp['configurePhase'] = "\n    configurePhase = ''" +\
                    "\n      " +\
                    ("\n      ".join(tmp['configurePhase'])) +\
                    "\n    '';"

            print TMPL_NIX_EXPR % tmp
        print TMPL_VERSION_END
