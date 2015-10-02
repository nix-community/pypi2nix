import click
import pypi2nix.stage1
import pypi2nix.parse_wheels


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def main(input_file):

    #
    # Stage 1
    #
    # from setup.py or buildout.cfg we create complete list of all requirements
    # needed.
    #
    click.secho('Stage1: Generating wheelshouse', fg='yellow')
    i = lambda x: input_file.endswith(x) and input_file or False
    if i('setup.py') or i('.cfg') or i('.txt'):
        wheels_dir = pypi2nix.stage1.do(input_file,
            )
    else:
        raise click.ClickException('You need to provide correct <input_file>.')

    #
    # Stage 2
    #
    # once we have all the metadata we can create wheels and install them, so
    # that metadata.json is produced for each package which we process to
    # extract dependencies for packages

    # returns a list of dicts, eg:
    # [
    #   dict(name=..., version=..., url=..., md5=..., deps=[...<list-of names>...]),
    #   ...
    # ]
    click.secho('Extracting metadata from %s' % wheels_dir, fg='yellow')
    metadata = pypi2nix.parse_wheels.do(wheels_dir)
    click.secho('Got metadata from %i packages' % len(packages), fg='green')

    #
    # Stage 3
    #
    # With all above we can now generate nix expressions
    #
    if wheels_file:
        click.secho('Converting %s to nix' % wheels_file, fg='yellow')
        nix_file = pypi2nix.wheels2nix.do(wheels_file)
        click.secho('Got %s' % nix_file, fg='green')
