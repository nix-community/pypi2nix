import sys
import copy
import json
import tempfile
import multiprocessing
from pypi2nix.buildout import run_buildout

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

DEFAULT_ENVIRONMENT = "py27"
ENVIRONMENTS = {
    u"py26": "python26Full",
    u"py27": "python27Full",
    u"py32": "python32",
    u"py33": "python33",
    u"pypy": "pythonPyPyFull",
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
                configs.append(temp_spec)
        else:
            spec['buildInputs'].append(ENVIRONMENTS[DEFAULT_ENVIRONMENT])
            spec['environment'] = DEFAULT_ENVIRONMENT
            configs.append(spec)

    results = []
    #pool = multiprocessing.Pool(processes=4)
    for config in configs:
        #results.append(pool.apply_async(run_buildout, [eggsdir, config]))
        results.append(run_buildout(eggsdir, config))

    for result in results:
        print '-' * 80
        print result
