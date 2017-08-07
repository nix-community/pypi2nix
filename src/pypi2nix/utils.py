import os
import json
import re
import shlex
import subprocess
from tempfile import TemporaryDirectory

import click
import jinja2
import requests


HERE = os.path.dirname(__file__)

TO_IGNORE = [
    "pip",
    "setuptools",
    "wheel",
    "zc.buildout",
    "zc.recipe.egg",
]

PYTHON_VERSIONS = {
    "2.6": "python26Full",
    "2.7": "python27Full",
    "3.2": "python32",
    "3.3": "python33",
    "3.4": "python34",
    "3.5": "python35",
    "3.6": "python36",
    "3": "python3",
    "pypy": "pypy",
}


def pretty_option(option):
    if option is None:
        return ''
    else:
        return ' [value: {}]'.format(
            type(option) in [list, tuple] and
            ' '.join(option) or
            option)


def safe(string):
    return string.replace('"', '\\"')


def cmd(command, verbose=False, stderr=subprocess.STDOUT):

    if isinstance(command, str):
        command = shlex.split(command)

    if verbose:
        click.echo('|-> ' + ' '.join(command))

    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=stderr,
    )

    out = []
    while True:
        line = p.stdout.readline().decode()
        if line == '' and p.poll() is not None:
            break
        if line != '':
            if verbose:
                click.echo('    ' + line.rstrip('\n'))
            out.append(line)

    return p.returncode, '\n'.join(out)


def create_command_options(options):
    command_options = []
    for name, value in options.items():
        if isinstance(value, str):
            command_options.append('--argstr {} "{}"'.format(name, value))
        elif isinstance(value, list) or isinstance(value, tuple):
            value = "[ %s ]" % (' '.join(['"%s"' % x for x in value]))
            command_options.append("--arg {} '{}'".format(name, value))
    return ' '.join(command_options)


def args_as_list(inputs):
    return list(filter(
        lambda x: x != '',
        (' '.join(inputs)).split(' ')
    ))


def prefetch_url(url):
    output = cmd(
        ['nix-prefetch-url', url],
        stderr=None,
    )
    return output[-1][:-1]


def prefetch_git(url, rev=None):
    command = ['nix-prefetch-git', url]

    if rev is not None:
        command += ['--rev', rev]
    try:
        completed_proc = subprocess.run(
            command,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        raise click.ClickException(
            'Could not find executable `nix-prefetch-git`.  '
            'Make sure it is installed correctly and available in '
            '$PATH.'
        )

    returncode = completed_proc.returncode

    if returncode != 0:
        raise click.ClickException(
            ('Could not fetch git repository at {url}, git returncode was '
             '{code}. stdout:\n{stdout}\nstderr:\n{stderr}').format(
                 url=url,
                 code=returncode,
                 stdout=completed_proc.stdout,
                 stderr=completed_proc.stderr,
            )
        )
    repo_data = json.loads(completed_proc.stdout)
    return repo_data


def get_latest_commit_from_github(owner, repo):
    url_template = 'https://api.github.com/repos/{owner}/{repo}/commits/master'
    request_url = url_template.format(
        owner=owner,
        repo=repo,
    )
    response = requests.get(request_url)
    return response.json()['sha']


def prefetch_github(owner, repo, rev=None):
    def select_hash_from_match(match):
        hash_untrimmed = match.group(1) or match.group(2)
        if hash_untrimmed:
            return hash_untrimmed[1:-1]
        else:
            return None

    calculated_rev = get_latest_commit_from_github(owner, repo)
    actual_rev = rev or calculated_rev
    templates_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(HERE + '/templates'),
    )
    template = templates_env.get_template('prefetch-github.nix.j2')
    nix_prefetch_code = template.render(
        owner=owner,
        repo=repo,
        rev=actual_rev,
        fake_hash='1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv',
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + '/prefetch-github.nix'
        with open(nix_filename, 'w') as f:
            f.write(nix_prefetch_code)
        returncode, output = cmd(['nix-build', nix_filename])
    r = re.compile(
        "|".join(
            ["output path .* has .* hash (.*) when .*",
             "fixed\-output derivation produced path .* with sha256 hash (.*) instead of the expected hash .*", # flake8: noqa: E501
            ]
        )
    )
    calculated_hash = None
    for line in output.splitlines():
        re_match = r.match(line)
        if not re_match:
            continue
        calculated_hash = select_hash_from_match(re_match)
        break
    if calculated_hash:
        return actual_rev, calculated_hash
    else:
        raise click.ClickException(
            (
                'Internal Error: Calculate hash value for sources '
                'in github repo {owner}/{repo}.\n\noutput was: {output}'
            ).format(owner=owner, repo=repo, output=output)
        )


def starts_with_any(s, prefixes):
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
    return False
