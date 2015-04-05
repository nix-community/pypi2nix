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

    if py_file:
        click.secho('Converting setup.py to requirements.txt', fg='yellow')
        txt_file = py2txt.do(py_file)
        click.secho('Got %s' % txt_file, fg='green')

    if cfg_file:
        click.secho('Converting %s to requirements.txt' % cfg_file, fg='yellow')
        txt_file = cfg2txt.do(cfg_file)
        click.secho('Got %s' % txt_file, fg='green')

    if txt_file:
        click.secho('Converting %s to json' % txt_file, fg='yellow')
        json_file = txt2json.do(txt_file)
        click.secho('Got %s' % json_file, fg='green')

    if json_file:
        click.secho('Converting %s to wheels' % json_file, fg='yellow')
        wheels_file = json2wheels.do(json_file, nix_path=nix_path)
        click.secho('Got %s' % wheels_file, fg='green')

    if wheels_file:
        click.secho('Converting %s to nix' % wheels_file, fg='yellow')
        nix_file = wheels2nix.do(wheels_file, nix_path=nix_path)
        click.secho('Got %s' % nix_file, fg='green')

    #defaultNix.do()
    #print '-> default.nix'
