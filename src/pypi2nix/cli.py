import click
import functools
import hashlib
import os
import random
import string
import tempfile
import shutil

import pypi2nix.stage1
import pypi2nix.stage2
import pypi2nix.stage3
import pypi2nix.utils


@click.command('pypi2nix')
@click.option('-I', '--nix-path',
              envvar='NIX_PATH',
              multiple=True,
              default=None,
              help=u'Add a path to the Nix expression search path. This '
                   u'option may be given multiple times. See the NIX_PATH '
                   u'environment variable for information on the semantics '
                   u'of the Nix search path. Paths added through -I take '
                   u'precedence over NIX_PATH.',
              )
@click.option('--basename',
              required=False,
              default=None,
              help=u'Basename which is used to generate files. By default '
                   u'it uses basename of provided file.',
              )
@click.option('-C', '--cache-dir',
              required=False,
              default=None,
              type=click.Path(exists=True, file_okay=True, writable=True,
                              resolve_path=True),
              help=u'Cache directory to be used for downloading packages.',
              )
@click.option('-E', '--extra-build-inputs',
              default=None,
              help=u'Extra build dependencies needed for installation of '
                   u'required python packages.'
              )
@click.option('-V', '--python-version',
              required=True,
              default="2.7",
              type=click.Choice(pypi2nix.utils.PYTHON_VERSIONS.keys()),
              help=u'Provide which python version we build for.',
              )
@click.option('-r', '--requirements',
              required=False,
              default=None,
              type=click.Path(exists=True, resolve_path=True),
              help=u'pip requirements.txt file',
              )
@click.option('-b', '--buildout',
              required=False,
              default=None,
              type=click.Path(exists=True),
              help=u'zc.buildout configuration file',
              )
@click.argument('specification',
                nargs=-1,
                required=False,
                default=None,
                )
def main(nix_path,
         basename,
         cache_dir,
         extra_build_inputs,
         python_version,
         requirements,
         buildout,
         specification,
         ):
    """SPECIFICATION should be requirements.txt (output of pip freeze).
    """

    # A user should specify only one of following options:
    #  * --requirements
    #  * --buildout
    #  * specifications
    if functools.reduce(
            lambda x, y: x + (y and 1 or 0),
            [requirements, buildout, specification != tuple()], 0) != 1:
        raise click.exceptions.UsageError(
            "Only one of following options must be specified:\n"
            " * -r/--requirements{}\n"
            " * -b/--buildout{}\n"
            " * SPECIFICATION{}\n".format(
                pypi2nix.utils.pretty_option(requirements),
                pypi2nix.utils.pretty_option(buildout),
                pypi2nix.utils.pretty_option(specification),
            ))

    # temporary pypi2nix folder and make sure it exists
    tmp_dir = os.path.join(tempfile.gettempdir(), 'pypi2nix')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # TODO: create requirements.txt from buildout.cfg
    if buildout:
        raise click.exceptions.ClickException(
            u'Not yet implemented!')

    # TODO: create requirements.txt from SPECIFICATION
    elif specification:
        raise click.exceptions.ClickException(
            u'Not yet implemented!')

    elif requirements:
        requirements_file = requirements
        requirements_name = os.path.splitext(os.path.basename(requirements))[0]

    if basename:
        requirements_name = basename

    if extra_build_inputs:
        extra_build_inputs = extra_build_inputs.split(' ')

    if not cache_dir:
        cache_dir = os.path.join(tmp_dir, 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    with open(requirements_file) as f:
        requirements = f.read()
    project_hash = hashlib.md5(
        (requirements_file + requirements).encode()).hexdigest()

    project_tmp_dir = os.path.join(tmp_dir, project_hash, 'tmp')
    if os.path.exists(project_tmp_dir):
        shutil.rmtree(project_tmp_dir)
    os.makedirs(project_tmp_dir)

    wheelhouse_dir = os.path.join(tmp_dir, project_hash, 'wheelhouse')
    if not os.path.exists(wheelhouse_dir):
        os.makedirs(wheelhouse_dir)

    click.echo('Downloading wheels and creating wheelhouse ...')

    wheels = pypi2nix.stage1.main(
        requirements_file=requirements_file,
        project_tmp_dir=project_tmp_dir,
        cache_dir=cache_dir,
        wheelhouse_dir=wheelhouse_dir,
        extra_build_inputs=extra_build_inputs,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        nix_path=nix_path,
    )

    click.echo('Extracting metadata ...')

    packages_metadata = pypi2nix.stage2.main(wheels)

    click.echo('Generating Nix expressions ...')

    pypi2nix.stage3.main(
        packages_metadata=packages_metadata,
        requirements_name=requirements_name,
        requirements_file=requirements_file,
        extra_build_inputs=extra_build_inputs,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
    )
