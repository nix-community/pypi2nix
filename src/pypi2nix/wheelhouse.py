import click
import hashlib
import os
import pypi2nix.cmd
import stat


def do(input_file, nix_path=None, extra_build_inputs=None, python="python27",
        cache_dir=None):

    if not input_file.endswith('.txt'):
        raise click.ClickException('You need to provide correct <input_file>.')

    if not os.path.exists(input_file):
        raise click.ClickException(
            'requirement file (%s) does not exists' % input_file)

    with open(input_file) as f:
        requirements = f.read()
    requirements = requirements.strip()

    current_dir = os.path.dirname(__file__)
    output = os.path.expanduser('~/.pypi2nix/out')

    if not cache_dir:
        cache_dir = os.path.expanduser(
            '/tmp/pypi2nix/cache/' + hashlib.md5(requirements).hexdigest())

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        os.chmod(
            cache_dir,
            stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
            stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH |
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

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
              '  --option build-use-chroot false'\
              '  --argstr requirements "{requirements}"'\
              '  --argstr cache "{cache_dir}"'\
              '  --argstr pythonVersion "{python}"'\
              '  --arg extraBuildInputs \'{extra_build_inputs}\''\
              '  {nix_path} -o {output} --show-trace'.format(**locals())

    returncode = pypi2nix.cmd.do(command)
    if returncode != 0:
        raise click.ClickException(
            u'While trying to run the command something went wrong.')

    return os.path.join(os.path.realpath(output), 'wheelhouse')
