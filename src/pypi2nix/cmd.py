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
        stderr=subprocess.STDOUT,
        )

    out = []
    while True:
        line = p.stdout.readline()
        if line == '' and p.poll() is not None:
            break
        if line != '':
            click.secho('    ' + line.rstrip('\n'), fg='yellow')
            out.append(line)

    return p.returncode
