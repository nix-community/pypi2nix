import os
import click

import pypi2nix.utils


def main(buildout_file,
         project_dir,
         buildout_cache_dir,
         extra_build_inputs,
         python_version,
         nix_path=None,
         ):
    """ Converts buildout.cfg specifiation into requirements.txt file
    """

    command = 'nix-shell {nix_file} {options} {nix_path} -K --show-trace --pure --run exit'.format(  # noqa
        nix_file=os.path.join(os.path.dirname(__file__), 'buildout.nix'),
        options=pypi2nix.utils.create_command_options(dict(
            buildout_file=buildout_file,
            project_dir=project_dir,
            buildout_cache_dir=buildout_cache_dir,
            extra_build_inputs=extra_build_inputs,
            python_version=python_version,
        )),
        nix_path=nix_path \
            and ' '.join('-I {}'.format(i) for i in nix_path) \
            or ''
    )

    returncode, output = pypi2nix.utils.cmd(command)
    if returncode != 0:
        click.echo(output)
        raise click.ClickException(
            u'While trying to run the command something went wrong.')

    return os.path.join(project__dir, 'buildout_requirements.txt')
