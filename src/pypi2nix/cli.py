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
@click.option('-v', '--verbose', count=True)
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
@click.option('--nix-shell',
              required=False,
              default='nix-shell',
              help=u'Path to nix-shell executable.',
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
              multiple=True,
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
              multiple=True,
              required=False,
              default=None,
              type=str,
              help=u'location/url to editable locations',
              )
def main(version,
         verbose,
         nix_shell,
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

    extra_build_inputs = ' '.join(extra_build_inputs)

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
    pip_build_dir = os.path.join(cache_dir, 'pip')

    if not os.path.exists(download_cache_dir):
        os.makedirs(download_cache_dir)

    if not os.path.exists(wheel_cache_dir):
        os.makedirs(wheel_cache_dir)

    if not os.path.exists(buildout_cache_dir):
        os.makedirs(buildout_cache_dir)

    if not os.path.exists(pip_build_dir):
        os.makedirs(pip_build_dir)

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

    def handle_requirements_file(project_dir, requirements_file):

        # we find new name for our requirements_file
        new_requirements_file = "%s/%s.txt" % (
            project_dir,
            hashlib.md5(requirements_file.encode()).hexdigest(),
        )

        # we open both files: f1 to read, f2 to write
        with open(requirements_file) as f1:
            with open(new_requirements_file, "w+") as f2:
                for requirements_line in f1.readlines():
                    if requirements_line.startswith("-e"):
                        requirements_line = "-e %s" % (
                            os.path.abspath(os.path.join(
                                os.path.dirname(requirements_file),
                                                requirements_line.strip()[3:]
                            ))
                        )
                    elif requirements_line.startswith("-r ./"):
                        requirements_file2 = os.path.abspath(os.path.join(
                            os.path.dirname(requirements_file),
                                            requirements_line.strip()[3:]
                        ))
                        new_requirements_file2 = handle_requirements_file(
                            project_dir, requirements_file2)
                        requirements_line = "-r " + new_requirements_file2
                    f2.write(requirements_line)

        return new_requirements_file

    requirements_files_tmp = []
    for requirements_file in requirements_files:
        if requirements_file in requirements:
            requirements_files_tmp.append(
                handle_requirements_file(project_dir, requirements_file))
        else:
            requirements_files_tmp.append(requirements_file)
    requirements_files = requirements_files_tmp

    click.echo('pypi2nix v{} running ...'.format(pypi2nix_version))
    click.echo('')

    if buildout:
        click.echo('Stage0: Generating requirements.txt from buildout configuration ...')
        buildout_requirements = pypi2nix.stage0.main(
            verbose=verbose,
            buildout_file=buildout,
            project_dir=project_dir,
            buildout_cache_dir=buildout_cache_dir,
            extra_build_inputs=extra_build_inputs,
            python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
            nix_shell=nix_shell,
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

        requirements_files = [editable_file] + requirements_files

    click.echo('Stage1: Downloading wheels and creating wheelhouse ...')

    requirements_frozen, wheels = pypi2nix.stage1.main(
        verbose=verbose,
        requirements_files=requirements_files,
        project_dir=project_dir,
        download_cache_dir=download_cache_dir,
        wheel_cache_dir=wheel_cache_dir,
        pip_build_dir=pip_build_dir,
        extra_build_inputs=extra_build_inputs,
        python_version=pypi2nix.utils.PYTHON_VERSIONS[python_version],
        nix_path=nix_path,
    )

    click.echo('Stage2: Extracting metadata from pypi.python.org ...')

    packages_metadata = pypi2nix.stage2.main(
        verbose=verbose,
        wheels=wheels,
        requirements_files=requirements_files,
        wheel_cache_dir=wheel_cache_dir
    )

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
