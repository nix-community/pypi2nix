import json
import argh
import argparse
import pypi2nix


@argh.arg('--dists', '-d', type=str, action='append')
@argh.arg('--ignores', '-i', default=[], type=str, action='append')
@argh.arg('--extends', '-e', default=None, type=open)
@argh.arg('--output', '-o', default=None, type=argparse.FileType('w+'))
def cli(dists, ignores, extends, output):

    if extends:
        extends = json.load(extends)

    expressions = pypi2nix.Pypi2Nix(dists, ignores, extends)

    if output:
        return output.write(str(expressions))
    else:
        return str(expressions).split('\n')


def main():
    argh.dispatch_command(cli)

if __name__ == '__main__':
    main()
