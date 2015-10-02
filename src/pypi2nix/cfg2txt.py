import os
import cmd


def do(cfg_file):
    out, err = cmd.do('nix-build %s/buildout.nix --argstr cfg %s' % (
        os.path.dirname(__file__), os.path.abspath(cfg_file)))

    # TODO: handle err

    return os.path.join(out.split('\n')[0], 'requirements.txt')

