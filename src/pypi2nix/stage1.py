import click
import glob
import os

import pypi2nix.utils


def main(verbose,
         requirements_files,
         project_dir,
         download_cache_dir,
         wheel_cache_dir,
         pip_build_dir,
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
            project_dir=project_dir,
            download_cache_dir=download_cache_dir,
            wheel_cache_dir=wheel_cache_dir,
            pip_build_dir=pip_build_dir,
            extra_build_inputs=extra_build_inputs,
            python_version=python_version,
        )),
        nix_path=nix_path \
            and ' '.join('-I {}'.format(i) for i in nix_path) \
            or ''
    )

    returncode, output = pypi2nix.utils.cmd(command, verbose != 0)
    if returncode != 0 or \
           output.endswith('ERROR: Failed to build one or more wheels'):
        if verbose == 0:
            click.echo(output)

        message = u'While trying to run the command something went wrong.'

        # trying to recognize the problem and provide more meanigful error
        # message
        no_matching_dist = "No matching distribution found for "
        if no_matching_dist in output:
            dist_name = output[output.find(no_matching_dist) + len(no_matching_dist):]
            dist_name = dist_name[:dist_name.find(' (from')]
            message = (
                "Most likely `%s` package does not have source (zip/tar.bz) "
                "distribution." % dist_name
            )

        raise click.ClickException(message)

    return (
        os.path.join(project_dir, 'requirements.txt'),
        glob.glob(os.path.join(project_dir, 'wheelhouse', '*.dist-info')),
    )
