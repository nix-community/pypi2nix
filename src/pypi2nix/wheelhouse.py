import os
import grp
import click
import pypi2nix.cmd
import tempfile


def do(input_file, nix_path=None, extra_build_inputs=None):

    if not input_file.endswith('.txt'):
        raise click.ClickException('You need to provide correct <input_file>.')

    input_file = os.path.abspath(input_file)
    current_dir = os.path.dirname(__file__)
    cache_dir = os.path.expanduser('~/.pypi2nix/cache')
    output = os.path.expanduser('~/.pypi2nix/out')

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    if nix_path:
        nix_path = ' '.join('-I {}'.format(i) for i in nix_path)
    else:
        nix_path = ''

    if extra_build_inputs:
        extra_build_inputs = '[ {} ]'.format(' '.join([
            '"{}"'.format(i) for i in extra_build_inputs.split()]))
    else:
        extra_build_inputs = '[]'

    command = 'nix-build {current_dir}/pip.nix'\
              '  --argstr requirementsFile "{input_file}"'\
              '  --argstr cache "{cache_dir}"'\
              '  --arg extraBuildInputs \'{extra_build_inputs}\''\
              '  {nix_path} -o {output} --show-trace'.format(**locals())

    returncode = pypi2nix.cmd.do(command)
    if returncode != 0:
        raise click.ClickException(
            u'While trying to run the command something went wrong.')

    return os.path.join(os.path.realpath(output), 'wheelhouse')
