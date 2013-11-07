import os
import sys
import json
import errno
import shlex
import subprocess


DEFAULT_ENVIRONMENT = u"2.7"
ENVIRONMENTS = {
    u"2.6": "python26Full",
    u"2.7": "python27Full",
    u"3.3": "python33",
}


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def prepare_spec(spec):
    if isinstance(spec, basestring):
        name = spec
        versions = {}
    else:
        name = spec['name']
        versions = spec.get('versions', {})
    return dict(
        name=name,
        versions=versions,
    )


def main():

    #
    # Open JSON file
    #
    try:
        f = open(sys.argv[1])
        specifications = json.load(f)
    except ValueError as e:
        print "File {} is not valid JSON file.".format(sys.argv[1])
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

    #
    # Figure out how many env we need to package packages for
    #
    environments = {}
    for spec in specifications:
        if type(spec) is dict and 'env' in spec:
            if isinstance(spec['env'], basestring):
                environments.setdefault(spec['env'], [])
                environments[spec['env']].append(prepare_spec(spec))
            else:
                for env in spec['env']:
                    if env not in ENVIRONMENTS:
                        print "'{}' not defined in ENVIRONMENTS ({})".format(
                            env, ENVIRONMENTS)
                        sys.exit(1)
                    environments.setdefault(env, [])
                    environments[env].append(prepare_spec(spec))
        else:
            environments.setdefault(DEFAULT_ENVIRONMENT, [])
            environments[DEFAULT_ENVIRONMENT].append(prepare_spec(spec))

    HOME = os.getenv('HOME')
    mkdir_p(HOME + '/.pypi2nix/profiles/')
    for env in environments:
        subprocess.check_output(
            "nix-env -p /home/rok/.pypi2nix/profiles/{} "
            "-f '<nixpkgs>' -iA {}".format(env, ENVIRONMENTS[env]),
            shell=True,
        )
        for spec in environments[env]:
            TODO:
            print spec
