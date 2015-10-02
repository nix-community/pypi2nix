import shlex
import subprocess
import click


def do(command):

    if isinstance(command, basestring):
        command = shlex.split(command)

    click.secho('|-> ' + ' '.join(command), fg='blue')
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )

    tmp = p.communicate()
    return [ p.returncode ] + list(tmp)
