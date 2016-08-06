import click
import hashlib
import os
import shutil
import tempfile

import pypi2nix.stage0
import pypi2nix.stage1
import pypi2nix.stage2
import pypi2nix.stage3
import pypi2nix.utils


@click.command('pypi2nix')
@click.option('--version',
              is_flag=True,
              help=u'Show version of pypi2nix',
              )
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
              default='requirements',
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
@click.option('-T', '--enable-tests',
              is_flag=True,
              help=u'Enable tests in generated packages.'
              )
@click.option('-V', '--python-version',
              required=False,
              default=None,
              type=click.Choice(pypi2nix.utils.PYTHON_VERSIONS.keys()),
              help=u'Provide which python version we build for.',
              )
@click.option('-r', '--requirements',
              required=False,
              default=None,
              multiple=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False,
                              resolve_path=True),
              help=u'pip requirements.txt file',
              )
@click.option('-b', '--buildout',
              required=False,
              default=None,
              type=click.Path(exists=True, resolve_path=True),
              help=u'zc.buildout configuration file',
              )
@click.option('-e', '--editable',
              required=False,
              default=None,
              multiple=True,
              type=str,
              help=u'location/url to editable locations',
              )
def main(version,
         nix_path,
         basename,
         cache_dir,
         extra_build_inputs,
         enable_tests,
         python_version,
         requirements,
         buildout,
         editable,
         ):
    """SPECIFICATION should be requirements.txt (output of pip freeze).
    """

    with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
        pypi2nix_version = f.read()

    if version:
        click.echo(pypi2nix_version)
        return

    python_versions = pypi2nix.utils.PYTHON_VERSIONS.keys()
    if not python_version:
        raise click.exceptions.UsageError(
            "Missing option \"-V\" / \"--python-version\".  Choose from " +
            (", ".join(python_versions)))

    # temporary pypi2nix folder and make sure it exists
    tmp_dir = os.path.join(tempfile.gettempdir(), 'pypi2nix')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    current_dir = os.getcwd()
    requirements_name = os.path.join(current_dir, basename)

    if extra_build_inputs:
        extra_build_inputs = extra_build_inputs.split(' ')

    if not cache_dir:
        cache_dir = os.path.join(tmp_dir, 'cache')

        download_cache_dir = os.path.join(cache_dir, 'download')
        wheel_cache_dir = os.path.join(cache_dir, 'wheel')
        buildout_cache_dir = os.path.join(cache_dir, 'buildout')

        if not os.path.exists(download_cache_dir):
            os.makedirs(download_cache_dir)

        if not os.path.exists(wheel_cache_dir):
            os.makedirs(wheel_cache_dir)

        if not os.path.exists(buildout_cache_dir):
            os.makedirs(buildout_cache_dir)

    requirements_files = []
    if requirements:
        requirements_files += requirements

    requirements_hash = ''
    for requirements_file in requirements_files:
        requirements_hash += requirements_file
        with open(requirements_file) as f:
            requirements_hash += f.read()

    if buildout:
        requirements_hash += buildout
        with open(buildout) as f:
            requirements_hash += f.read()

    project_hash = hashlib.md5(requirements_hash.encode()).hexdigest()

    project_dir = os.path.join(tmp_dir, project_hash)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)

    click.echo('')
    click.echo('pypi2nix v{} running ...'.format(pypi2nix_version))

    if buildout:
        click.echo('Stage0: Generating requirements.txt from buildout configuration ...')
        buildout_requirements = pypi2nix.stage0.main(
            buildout_file=buildout,
            project_dir=project_dir,
            buildout_cache_dir=buildout_cache_dir,
            extra_build_inputs=extra_build_inputs,
            python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
            nix_path=nix_path,
        )
        requirements_files.append(buildout_requirements)

    if editable:
        editable_file = os.path.join(tmp_dir, 'editable.txt')
        with open(editable_file, 'w+') as f:
            for item in editable:
                if os.path.isdir(item):
                    f.write('-e %s\n' % item)
                elif os.path.isfile(item):
                    f.write('-e %s\n' % os.path.dirname(item))
                else:
                    f.write('%s\n' % item)

        requirements_files.append(editable_file)

    click.echo('Stage1: Downloading wheels and creating wheelhouse ...')

    requirements_frozen, wheels = pypi2nix.stage1.main(
        requirements_files=requirements_files,
        project_dir=project_dir,
        download_cache_dir=download_cache_dir,
        wheel_cache_dir=wheel_cache_dir,
        extra_build_inputs=extra_build_inputs,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        nix_path=nix_path,
    )

    click.echo('Stage2: Extracting metadata from pypi.python.org ...')

    packages_metadata = pypi2nix.stage2.main(
        wheels, requirements_files, wheel_cache_dir)

    click.echo('Stage3: Generating Nix expressions ...')

    pypi2nix.stage3.main(
        packages_metadata=packages_metadata,
        requirements_name=requirements_name,
        requirements_files=requirements_files,
        requirements_frozen=requirements_frozen,
        extra_build_inputs=extra_build_inputs,
        enable_tests=enable_tests,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        current_dir=current_dir,
    )


    click.echo('')
    click.echo('Nix expressions generated successfully.')
    click.echo('')
    click.echo('To start development run:')
    click.echo('    nix-shell requirements.nix -A interpreter')
    click.echo('')
    click.echo('More information you can find at')
    click.echo('    https://github.com/garbas/pypi2nix')
    click.echo('')
