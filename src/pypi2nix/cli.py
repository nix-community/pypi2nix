import sys
import click
import pypi2nix.txt2json
import pypi2nix.json2wheels
import pypi2nix.wheels2nix


@click.command()
@click.option('--nix-path', '-I', type=str, default='')
@click.argument('input', type=click.Path(exists=True))
def main(input, nix_path):
    py_file = None
    cfg_file = None
    txt_file = None
    json_file = None
    wheels_file = None
    nix_file = None

    # detect input and start 
    if input.endswith('setup.py'):
        py_file = input
    elif input.endswith('.cfg'):
        cfg_file = input
    elif input.endswith('.txt'):
        txt_file = input
    elif input.endswith('.json'):
        json_file = input
    elif input.endswith('.wheels'):
        wheels_file = input
    else:
        print '<input> was not correct type. check help for more info.'
        sys.exit(1)

    if cfg_file:
        json_file = pypi2nix.cfg2txt.do(txt_file)

    if txt_file:
        json_file = pypi2nix.txt2json.do(txt_file)

    if json_file:
        wheels_file = pypi2nix.json2wheels.do(json_file, nix_path=nix_path)

    if wheels_file:
        nix_file = pypi2nix.wheels2nix.do(wheels_file, nix_path=nix_path)

    #defaultNix.do()
    #print '-> default.nix'
