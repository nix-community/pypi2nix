import os
import click
import random
import string

from pypi2nix.stage1 import download_wheels_and_create_wheelhouse
from pypi2nix.stage2 import extract_metadata_from_wheelhouse
from pypi2nix.stage3 import generate_nix_expressions
from pypi2nix.utils import PYTHON_VERSIONS, compose


@click.command()
@click.option(
    '-I', '--nix-path',
    envvar='NIX_PATH',
    multiple=True,
    default=None,
    help=u'Add a path to the Nix expression search path. This option may be '
         u'given multiple times. See the NIX_PATH environment variable for '
         u'information on the semantics of the Nix search path. Paths added '
         u'through -I take precedence over NIX_PATH.',
)
@click.option(
    '-r', '--requirements',
    required=False,
    default=None,
    type=click.Path(exists=True),
    help=u'',
)
@click.option(
    '-b', '--buildout',
    required=False,
    default=None,
    type=click.Path(exists=True),
    help=u'TODO',
)
@click.option(
    '--name',
    required=False,
    default=None,
    help=u'TODO',
)
@click.option(
    '-C', '--cache-dir',
    required=False,
    default=None,
    type=click.Path(exists=True, file_okay=True, writable=True,
                    resolve_path=True),
    help=u'Cache directory to be used for downloading packages.',
)
@click.option(
    '-E', '--extra-build-inputs',
    default=None,
    help=u'Extra build dependencies needed for installation of required '
         u'python packages.'
)
@click.option(
    '-V', '--python-version',
    required=True,
    default="2.7",
    type=click.Choice(PYTHON_VERSIONS.keys()),
    help=u'Provide which python version we build for.',
)
@click.argument(
    'specification',
    nargs=-1,
    required=False,
    default=None,
)
def main(specification, name, requirements, buildout, nix_path,
         extra_build_inputs, python_version, cache_dir):
    """INPUT_FILE should be requirements.txt (output of pip freeze).
    """

    # ensure that working folder exists
    home_dir = os.path.expanduser('~/.pypi2nix')
    if not os.path.isdir(home_dir):
        os.makedirs(home_dir)

    # adjust input_name/input_file based on the inputs
    if buildout:
        raise click.exceptions.ClickException(
            u'Not yet implemented!')

    elif requirements:
        input_file = requirements
        input_name = os.path.splitext(os.path.basename(input_file))[0]

    elif specification:
        input_name = '_'.join(specification)
        input_file = os.path.expanduser(os.path.join(
            '~/.pypi2nix', 'requirements-%s.txt' % (''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(6)))))
        with open(input_file, 'w+') as f:
            f.write('\n'.join(specification))

    else:
        raise click.exceptions.UsageError(
            u'Please tell what you want to be packages by specifying `-b` '
            u'(buildout.cfg), `-r` (requirements.txt) or by providing '
            u'package specification as a argument of pypi2nix command')

    compose(
        download_wheels_and_create_wheelhouse(
            nix_path=nix_path,
            extra_build_inputs=extra_build_inputs,
            python=PYTHON_VERSIONS[python_version],
            cache_dir=cache_dir),
        extract_metadata_from_wheelhouse,
        generate_nix_expressions(
            input_name=input_name,
            input_file=input_file,
            python_version=python_version),
    )(input_file=input_file)
