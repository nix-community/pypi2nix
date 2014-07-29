import click

from pypi2nix import txt2json
from pypi2nix import json2nix


@click.command()
@click.argument('input', type=click.Path(exists=True))
def main(input):
    print '-> requirements.txt'

    txt2json.do(input)

    print '-> generated.json'

    json2nix.do()

    print '-> generated.nix'

    #defaultNix.do()

    print '-> default.nix'
