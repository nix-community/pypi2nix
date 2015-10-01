import os
import cmd


def do(py_file):
    out, err = cmd.do('nix-build %s/buildout.nix --argstr path %s' % (
        os.path.dirname(__file__), os.path.dirname(py_file)))

    # TODO: handle err

    return os.path.join(out.split('\n')[0], 'requirements.txt')

