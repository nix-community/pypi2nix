import click
import hashlib
import os

from pypi2nix.utils import curry, cmd


@curry
def download_wheels_and_create_wheelhouse(
        input_file, nix_path=None, extra_build_inputs=None, python="python27",
        cache_dir=None):
    '''from setup.py or buildout.cfg we create complete list of all
       requirements needed.
    '''

    click.echo('Downloading wheels and creating wheelhouse')

    if not os.path.exists(input_file):
        raise click.ClickException(
            'requirement file (%s) does not exists' % input_file)

    current_dir = os.path.dirname(__file__)
    output = os.path.expanduser('~/.pypi2nix/out')

    with open(input_file) as f:
        requirements = f.read()
    requirements = requirements.strip()

    if not cache_dir:
        cache_dir = os.path.expanduser(
            '/tmp/pypi2nix/cache/' + hashlib.md5(requirements).hexdigest())

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    wheelhouse_dir = os.path.expanduser(
        '/tmp/pypi2nix/wheelhouse/' + hashlib.md5(requirements).hexdigest())
    if not os.path.exists(wheelhouse_dir):
        os.makedirs(wheelhouse_dir)

    if nix_path:
        nix_path = ' '.join('-I {}'.format(i) for i in nix_path)
    else:
        nix_path = ''

    if extra_build_inputs:
        extra_build_inputs = '[ {} ]'.format(' '.join([
            '"{}"'.format(i) for i in extra_build_inputs.split()]))
    else:
        extra_build_inputs = '[]'

    command = 'nix-shell {current_dir}/pip.nix'\
              '  --argstr requirements "{input_file}"'\
              '  --argstr cache "{cache_dir}"'\
              '  --argstr wheelhouse "{wheelhouse_dir}"'\
              '  --arg extraBuildInputs \'{extra_build_inputs}\''\
              '  --argstr pythonVersion "{python}"'\
              '  {nix_path} --show-trace --run exit'.format(**locals())

    returncode = cmd(command)
    if returncode != 0:
        raise click.ClickException(
            u'While trying to run the command something went wrong.')

    return wheelhouse_dir
