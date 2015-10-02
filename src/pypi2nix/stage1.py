import os
import click
import pypi2nix.cmd


def do(input_file):
    i = lambda x: input_file.endswith(x) and input_file or False

    input_file_type = None
    if i('setup.py') or i('.txt'):
        input_file_type = 'pip'
    elif i('.cfg'):
        input_file_type = 'buildout'
    else:
        raise click.ClickException('Wrong input_file type!')

    code, out, err = pypi2nix.cmd.do(
        'nix-build %s/%s.nix --argstr input_file %s' % (
            os.path.dirname(__file__),
            input_file_type,
            os.path.abspath(input_file),
        ))

    if code != 0 and err:
        raise click.ClickException(err.decode('utf-8'))

    return os.path.join(out.split('\n')[0], 'wheelhouse')
