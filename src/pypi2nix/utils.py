import hashlib
import json
import os
import shlex
import subprocess

import click
import requests
from nix_prefetch_github import nix_prefetch_github

HERE = os.path.dirname(__file__)

TO_IGNORE = ["pip", "setuptools", "wheel", "zc.buildout", "zc.recipe.egg"]

PYTHON_VERSIONS = {
    "2.6": "python26Full",
    "2.7": "python27Full",
    "3.2": "python32",
    "3.3": "python33",
    "3.4": "python34",
    "3.5": "python35",
    "3.6": "python36",
    "3.7": "python37",
    "3": "python3",
    "pypy": "pypy",
}


def pretty_option(option):
    if option is None:
        return ""
    else:
        return " [value: {}]".format(
            type(option) in [list, tuple] and " ".join(option) or option
        )


def safe(string):
    return string.replace('"', '\\"')


def cmd(command, verbose=False, stderr=subprocess.STDOUT):

    if isinstance(command, str):
        command = shlex.split(command)

    if verbose:
        click.echo("|-> " + " ".join(command))

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=stderr)

    out = []
    while True:
        line = p.stdout.readline().decode()
        if line == "" and p.poll() is not None:
            break
        if line != "":
            if verbose:
                click.echo("    " + line.rstrip("\n"))
            out.append(line)

    return p.returncode, "\n".join(out)


def create_command_options(options, list_form=False):
    command_options = []
    for name, value in options.items():
        if isinstance(value, str):
            command_options.append("--argstr")
            command_options.append(name)
            command_options.append(value if list_form else '"{}"'.format(value))
        elif isinstance(value, list) or isinstance(value, tuple):
            value = "[ %s ]" % (" ".join(['"%s"' % x for x in value]))
            command_options.append("--arg")
            command_options.append(name)
            command_options.append(value if list_form else "'{}'".format(value))
    return command_options if list_form else " ".join(command_options)


def args_as_list(inputs):
    return list(filter(lambda x: x != "", (" ".join(inputs)).split(" ")))


def prefetch_git(url, rev=None):
    command = ["nix-prefetch-git", url]

    if rev is not None:
        command += ["--rev", rev]
    try:
        completed_proc = subprocess.run(
            command,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        raise click.ClickException(
            "Could not find executable `nix-prefetch-git`.  "
            "Make sure it is installed correctly and available in "
            "$PATH."
        )

    returncode = completed_proc.returncode

    if returncode != 0:
        raise click.ClickException(
            (
                "Could not fetch git repository at {url}, git returncode was "
                "{code}. stdout:\n{stdout}\nstderr:\n{stderr}"
            ).format(
                url=url,
                code=returncode,
                stdout=completed_proc.stdout,
                stderr=completed_proc.stderr,
            )
        )
    repo_data = json.loads(completed_proc.stdout)
    return repo_data


def prefetch_hg(url, rev=None, verbose=False):
    command = ["nix-prefetch-hg", url] + ([rev] if rev else [])
    return_code, output = cmd(command, verbose)
    if return_code != 0:
        raise click.ClickException(
            " ".join(
                [
                    "Could not fetch hg repository at {url}, returncode was {code}."
                    "stdout:\n {stdout}"
                ]
            ).format(url=url, code=return_code, stdout=output)
        )
    HASH_PREFIX = "hash is "
    REV_PREFIX = "hg revision is "
    hash_value = None
    revision = None
    for output_line in output.splitlines():
        output_line = output_line.strip()
        if output_line.startswith(HASH_PREFIX):
            hash_value = output_line[len(HASH_PREFIX) :].strip()
        elif output_line.startswith(REV_PREFIX):
            revision = output_line[len(REV_PREFIX) :].strip()

    if hash_value is None:
        raise click.ClickException(
            "Could not determine the hash from ouput:\n{output}".format(output=output)
        )
    if revision is None:
        raise click.ClickException(
            "Could not determine the revision from ouput:\n{output}".format(
                output=output
            )
        )
    return {"sha256": hash_value, "revision": revision}


def prefetch_github(owner, repo, rev=None):
    return nix_prefetch_github(owner, repo, rev=rev)


def escape_double_quotes(text):
    return text.replace('"', '\\"')


def prefetch_url(url, verbose=False):
    returncode, output = cmd(["nix-prefetch-url", url], verbose=verbose)
    return output.splitlines()[2]


def download_file(url, filename, chunk_size=2048):
    r = requests.get(url, stream=True, timeout=None)
    r.raise_for_status()  # TODO: handle this nicer

    with open(filename, "wb") as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def md5_sum_of_files_with_file_names(paths):
    hash_sum = hashlib.md5()
    for path in paths:
        hash_sum.update(path.encode())
        with open(path, "rb") as f:
            hash_sum.update(f.read())
    return hash_sum.hexdigest()
