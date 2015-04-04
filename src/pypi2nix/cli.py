import sys
import click
import py2txt
import txt2json
import json2wheels
import wheels2nix


@click.command()
@click.option('--nix-path', '-I', type=str, default='')
@click.argument('input_file', type=click.Path(exists=True))
def main(input_file, nix_path):
    i = lambda end: input_file.endswith(end)

    py_file = input_file if i('setup.py') else None
    cfg_file = input_file if i('.cfg') else None
    txt_file = input_file if i('.txt') else None
    json_file = input_file if i('.json') else None
    wheels_file = input_file if i('.wheels') else None
    nix_file = None

    if not (py_file or cfg_file or txt_file or json_file or wheels_file):
        raise Exception(
            '<input_file> was not correct type. check help for more info.')

    if cfg_file:
        json_file = cfg2txt.do(cfg_file)

    if txt_file:
        json_file = txt2json.do(txt_file)

    if json_file:
        wheels_file = json2wheels.do(json_file, nix_path=nix_path)

    if wheels_file:
        nix_file = wheels2nix.do(wheels_file, nix_path=nix_path)

    #defaultNix.do()
    #print '-> default.nix'
