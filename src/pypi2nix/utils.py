import json
import os
import shlex
import subprocess
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import click
from nix_prefetch_github import nix_prefetch_github

from pypi2nix.logger import Logger

NixOption = Union[str, List[str], bool]

HERE = os.path.dirname(__file__)


def pretty_option(option: Optional[str]) -> str:
    if option is None:
        return ""
    else:
        return " [value: {}]".format(
            type(option) in [list, tuple] and " ".join(option) or option
        )


def safe(string: str) -> str:
    return string.replace('"', '\\"')


def cmd(
    command: Union[str, List[str]], logger: Logger, stderr: Optional[int] = None
) -> Tuple[int, str]:
    if isinstance(command, str):
        command = shlex.split(command)

    logger.debug("|-> " + " ".join(map(shlex.quote, command)))

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=stderr)

    try:
        out = []
        while True:
            line = p.stdout.readline().decode()
            if line == "" and p.poll() is not None:
                break
            if line != "":
                logger.debug("    " + line.rstrip("\n"))
                out.append(line)
    except Exception:
        p.kill()
        raise
    finally:
        p.communicate()
    return p.returncode, "".join(out)


def create_command_options(options: Dict[str, NixOption],) -> List[str]:
    command_options = []
    for name, value in options.items():
        if isinstance(value, str):
            command_options.append("--argstr")
            command_options.append(name)
            command_options.append(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            value = "[ %s ]" % (" ".join(['"%s"' % x for x in value]))
            command_options.append("--arg")
            command_options.append(name)
            command_options.append(value)
        elif isinstance(value, bool):
            command_options.append("--arg")
            command_options.append(name)
            command_options.append("true" if value else "false")
    return command_options


def args_as_list(inputs: List[str]) -> List[str]:
    return list(filter(lambda x: x != "", (" ".join(inputs)).split(" ")))


def prefetch_git(url: str, rev: Optional[str] = None) -> Dict[str, str]:
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
    return repo_data  # type: ignore


def prefetch_hg(url: str, logger: Logger, rev: Optional[str] = None) -> Dict[str, str]:
    command = ["nix-prefetch-hg", url] + ([rev] if rev else [])
    return_code, output = cmd(command, logger, stderr=subprocess.STDOUT)
    if return_code != 0:
        raise click.ClickException(
            " ".join(
                [
                    "Could not fetch hg repository at {url}, returncode was {code}."
                    "output:\n {output}"
                ]
            ).format(url=url, code=return_code, output=output)
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


def prefetch_github(owner: str, repo: str, rev: Optional[str] = None) -> Dict[str, str]:
    return nix_prefetch_github(owner, repo, rev=rev)


def escape_double_quotes(text: str) -> str:
    return text.replace('"', '\\"')


def prefetch_url(url: str, logger: Logger) -> str:
    returncode, output = cmd(
        ["nix-prefetch-url", url], logger, stderr=subprocess.DEVNULL
    )
    return output.rstrip()
