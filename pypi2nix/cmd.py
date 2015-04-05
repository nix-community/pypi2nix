import shlex
import subprocess


def do(command):

    if isinstance(command, basestring):
        command = shlex.split(command)

    print ' '.join(command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )

    return p.communicate()
