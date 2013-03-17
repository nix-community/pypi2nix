#from distutils2.errors import IrrationalVersionError
#from distutils2.pypi.errors import ProjectNotFound
#from python2nix.config import IGNORE_PACKAGES
#from python2nix.config import POST_TMPL
#from python2nix.config import PRE_TMPL
#from python2nix.config import SYSTEM_PACKAGES
#from python2nix.config import TMPL
#from python2nix.utils import to_dict
#from python2nix.utils import to_nix_dict
#
#import sys

import argh
import python2nix


@argh.arg('--dist', '-d')
@argh.arg('--ignores', '-i', default=[], type=str, action='append')
@argh.arg('--extends', '-e', default=None)
@argh.arg('--output', '-o', default=None)
def pypi2nix(dist, ignores, extends, output):
    """
    """
    expressions = python2nix.Pypi2Nix(dist, ignores, extends)
    if output:
        return expressions.to_file(output)
    else:
        return expressions.to_string().split('\n')


def pypi():
    argh.dispatch_command(pypi2nix)

if __name__ == '__main__':
    pypi()
