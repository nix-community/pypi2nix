import click
import glob
import hashlib
import os
import tempfile

import pypi2nix.utils


def create_command_options(options):
    command_options = []
    for name, value in options.items():
        if isinstance(value, str):
            command_options.append('--argstr {} "{}"'.format(name, value))
        elif isinstance(value, list):
            value = "[ %s ]" % (' '.join(['"%s"' % x for x in value]))
            command_options.append("--arg {} '{}'".format(name, value))
    return ' '.join(command_options)


def main(requirements_file,
         project_tmp_dir,
         cache_dir,
         wheelhouse_dir,
         extra_build_inputs,
         python_version,
         nix_path=None
         ):
    """Create a complete (pip freeze) requirements.txt and a wheelhouse from
       a user provided requirements.txt.
    """

    command = 'nix-shell {pip} {options} {nix_path} --show-trace --run exit'.format(  # noqa
        pip=os.path.join(os.path.dirname(__file__), 'pip.nix'),
        options=create_command_options(dict(
            requirements_file=requirements_file,
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

    top_level = []
    with open(requirements_file) as f:
        line = f.read()
        for sep in ['#', ' ', '==', '<=', '>=', '<', '>']:
            line = line.split(sep)[0]
        line = line.strip()
        if line:
            top_level.append(line)

    return top_level, glob.glob(os.path.join(wheelhouse_dir, '*.dist-info'))
