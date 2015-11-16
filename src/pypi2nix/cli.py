import os
import click
import pypi2nix.wheelhouse
import pypi2nix.parse_wheels
import pypi2nix.stage3


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
    '-E', '--extra-build-inputs',
    default=None,
    help=u'TODO: add help message.'
)
@click.argument('input_file', type=click.Path(exists=True))
def main(input_file, nix_path, extra_build_inputs):
    '''
        INPUT_FILE should be requirements.txt (output of pip freeze).
    '''

    #
    # Stage 1
    #
    # from setup.py or buildout.cfg we create complete list of all requirements
    # needed.
    #
    click.secho('Downloading wheels and creating wheelhouse', fg='green')
    wheels_dir = pypi2nix.wheelhouse.do(
        input_file, nix_path, extra_build_inputs)

    #
    # Stage 2
    #
    # once we have all the metadata we can create wheels and install them, so
    # that metadata.json is produced for each package which we process to
    # extract dependencies for packages
    #
    click.secho(
        'Stage2: Extracting metadata from {}'.format(wheels_dir), fg='green')
    metadata = pypi2nix.parse_wheels.do(wheels_dir)
    click.secho(
        'Got metadata from {:d} packages'.format(len(metadata)), fg='green')

    #
    # Stage 3
    #
    # With all above we can now generate nix expressions
    #
    base_dir = os.path.dirname(input_file)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    default_file = os.path.join(base_dir, '{}.nix'.format(base_name))
    generate_file = os.path.join(
        base_dir, '{}_generated.nix'.format(base_name))
    overwrite_file = os.path.join(
        base_dir, '{}_overwrite.nix'.format(base_name))

    with open(input_file) as f:
        pypi2nix.stage3.do(metadata, generate_file)

    if not os.path.exists(overwrite_file):
        with open(overwrite_file, 'wa+') as f:
            write = lambda x: f.write(x + '\n')

            write("{ pkgs, self, generated, pythonPackages}:")
            write("let")
            write("  inherit (pkgs.lib) overrideDerivation;")
            write("  inherit (pythonPackages) buildPythonPackage python;")
            write("in {")
            write("}")

    if not os.path.exists(default_file):
        with open(default_file, 'wa+') as f:
            write = lambda x: f.write(x + '\n')
            write("{ }:")
            write("let")
            write("  pkgs = import <nixpkgs> { };")
            write("  pythonPackages = pkgs.python27Packages;")
            write("  generated = import ./sentry_generated.nix { "
                  "inherit pkgs self pythonPackages; };")
            write("  overrides = import ./sentry_overwrite.nix { "
                  "inherit pkgs self generated pythonPackages; };")
            write("  self = generated // overrides;")
            write("in self")
