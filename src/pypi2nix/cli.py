import click
import pypi2nix.cfg2txt
import pypi2nix.json2wheels
import pypi2nix.parse_wheels
import pypi2nix.py2txt
import pypi2nix.txt2json


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def main(input_file):

    i = lambda end: input_file.endswith(end) and input_file or None

    py_file = i('setup.py')
    cfg_file = i('.cfg')
    txt_file = i('.txt')

    #
    # Stage 1
    #
    # from setup.py or buildout.cfg we create complete list of all requirements
    # needed.
    #
    if py_file:
        click.secho('Converting setup.py to requirements.txt', fg='yellow')
        wheels_dir = pypi2nix.py2txt.do(py_file)
        click.secho('Got %s' % py_file, fg='green')

    elif cfg_file:
        click.secho('Converting %s to requirements.txt' % cfg_file, fg='yellow')
        wheels_dir = pypi2nix.cfg2txt.do(cfg_file)
        click.secho('Got %s' % cfg_file, fg='green')

    elif txt_file:
        click.secho('Converting %s to requirements.txt' % cfg_file, fg='yellow')
        wheels_dir = pypi2nix.cfg2txt.do(cfg_file)
        click.secho('Got %s' % txt_file, fg='green')
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


if __name__ == "__main__":
    main()
