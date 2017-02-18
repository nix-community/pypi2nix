import click
import glob
import os
import sys
import urllib

import pypi2nix.utils


HERE = os.path.dirname(__file__)


def main(verbose,
         requirements_files,
         project_dir,
         download_cache_dir,
         wheel_cache_dir,
         pip_build_dir,
         extra_build_inputs,
         python_version,
         nix_path=None,
         nix_shell='nix-shell',
         setup_requires=[],
         extra_env='',
         ):
    """Create a complete (pip freeze) requirements.txt and a wheelhouse from
       a user provided requirements.txt.
    """

    if nix_path:
        nix_path = ' '.join('-I {}'.format(i) for i in nix_path)
    else:
        nix_path = ''

    if extra_env:
        nix_instantiate = 'nix-instantiate'
        if os.path.exists(nix_shell):
            nix_instantiate = \
                os.path.abspath(os.path.join(
                    os.path.dirname(nix_path),
                    nix_instantiate
                ))
        command_env = '%s %s --eval --expr \'let pkgs = import <nixpkgs> {}; in "%s"\'' % (  # noqa
            nix_instantiate,
            nix_path,
            extra_env.replace('"', '\\"')
        )
        returncode, output = pypi2nix.utils.cmd(command_env, verbose != 0)
        if returncode != 0:
            if verbose == 0:
                click.echo(output)
            raise click.ClickException('Failed to interpret extra_env')
        extra_env = output.split('\n')[-2].strip()[1:-1]

    command = '{nix_shell} {nix_file} {nix_options} {nix_path} --show-trace --pure --run exit'.format(  # noqa
        nix_shell=nix_shell,
        nix_file=os.path.join(os.path.dirname(__file__), 'pip.nix'),
        nix_options=pypi2nix.utils.create_command_options(dict(
            requirements_files=requirements_files,
            project_dir=project_dir,
            download_cache_dir=download_cache_dir,
            wheel_cache_dir=wheel_cache_dir,
            pip_build_dir=pip_build_dir,
            extra_build_inputs=extra_build_inputs,
            extra_env=extra_env,
            python_version=python_version,
            setup_requires=setup_requires,
        )),
        nix_path=nix_path,
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
            dist_name = output[
                output.find(no_matching_dist) + len(no_matching_dist):
            ]
            dist_name = dist_name[:dist_name.find(' (from')]
            message = (
                "Most likely `%s` package does not have source (zip/tar.bz) "
                "distribution." % dist_name
            )

        # if error is unknown then we ask to report an issue
        else:
            if click.confirm('Do you want to report above issue (a browser '
                             'will open with prefilled details of issue)?'):
                title = "Error when running pypi2nix command"
                body = "# Description\n\n<detailed description of error "
                "here>\n\n"
                body += "# Traceback \n\n```bash\n"
                body += "% pypi2nix --version\n"
                with open(os.path.join(HERE, 'VERSION')) as f:
                    body += f.read() + "\n"
                body += "% pypi2nix " + ' '.join(sys.argv[1:]) + "\n"
                body += output + "\n```\n"
                click.launch(
                    'https://github.com/garbas/pypi2nix/issues/new?%s' % (
                        urllib.parse.urlencode(dict(title=title, body=body))
                    )
                )

        raise click.ClickException(message)

    return (
        os.path.join(project_dir, 'requirements.txt'),
        glob.glob(os.path.join(project_dir, 'wheelhouse', '*.dist-info')),
    )
