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
