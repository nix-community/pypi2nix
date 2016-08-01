import click
import glob
import os

import pypi2nix.utils


def main(requirements_files,
         project_tmp_dir,
         cache_dir,
         wheelhouse_dir,
         extra_build_inputs,
         python_version,
         nix_path=None,
         ):
    """Create a complete (pip freeze) requirements.txt and a wheelhouse from
       a user provided requirements.txt.
    """

    command = 'nix-shell {nix_file} {options} {nix_path} --show-trace --pure --run exit'.format(  # noqa
        nix_file=os.path.join(os.path.dirname(__file__), 'pip.nix'),
        options=pypi2nix.utils.create_command_options(dict(
            requirements_files=requirements_files,
            project_tmp_dir=project_tmp_dir,
            cache_dir=cache_dir,
            wheelhouse_dir=wheelhouse_dir,
            extra_build_inputs=extra_build_inputs,
            python_version=python_version,
        )),
        nix_path=nix_path \
            and ' '.join('-I {}'.format(i) for i in nix_path) \
            or ''
    )

    returncode = pypi2nix.utils.cmd(command)
    if returncode != 0:
        raise click.ClickException(
            u'While trying to run the command something went wrong.')

    return glob.glob(os.path.join(wheelhouse_dir, '*.dist-info'))
