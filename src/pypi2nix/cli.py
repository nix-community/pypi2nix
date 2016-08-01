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

    if version:
        with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
            click.echo(f.read())
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

    project_dir = os.getcwd()
    requirements_name = os.path.join(project_dir, basename)

    if extra_build_inputs:
        extra_build_inputs = extra_build_inputs.split(' ')

    if not cache_dir:
        cache_dir = os.path.join(tmp_dir, 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

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

    project_tmp_dir = os.path.join(tmp_dir, project_hash, 'tmp')
    if os.path.exists(project_tmp_dir):
        shutil.rmtree(project_tmp_dir)
    os.makedirs(project_tmp_dir)

    if buildout:
        buildout_requirements = pypi2nix.stage0.main(
            buildout_file=buildout,
            project_tmp_dir=project_tmp_dir,
            cache_dir=cache_dir,
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

    wheelhouse_dir = os.path.join(tmp_dir, project_hash, 'wheelhouse')
    if not os.path.exists(wheelhouse_dir):
        os.makedirs(wheelhouse_dir)

    click.echo('Downloading wheels and creating wheelhouse ...')

    wheels = pypi2nix.stage1.main(
        requirements_files=requirements_files,
        project_tmp_dir=project_tmp_dir,
        cache_dir=cache_dir,
        wheelhouse_dir=wheelhouse_dir,
        extra_build_inputs=extra_build_inputs,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        nix_path=nix_path,
    )

    click.echo('Extracting metadata ...')

    packages_metadata = pypi2nix.stage2.main(
        wheels, requirements_files, cache_dir)

    click.echo('Generating Nix expressions ...')

    pypi2nix.stage3.main(
        packages_metadata=packages_metadata,
        requirements_name=requirements_name,
        requirements_files=requirements_files,
        extra_build_inputs=extra_build_inputs,
        enable_tests=enable_tests,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        project_dir=project_dir,
    )
