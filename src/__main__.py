# -*- coding: utf-8 -*-

import sys

from pypi2nix.cli import main
from zc.buildout import buildout


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == buildout:
        buildout.main(sys.argv[2:])
    else:
        main(sys.argv[1:])
