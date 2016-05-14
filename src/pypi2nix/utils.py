import click
import functools
import shlex
import subprocess


TO_IGNORE = ["setuptools", "wheel"]

PYTHON_VERSIONS = {
    "2.6": "python26",
    "2.7": "python27",
    "3.2": "python32",
    "3.3": "python33",
    "3.4": "python34",
    "3.5": "python35",
    "pypy": "pypy",
}


def safe(string):
    return string.replace('"', '\\"')


def compose(*functions):
    """
    https://mathieularose.com/function-composition-in-python

    >>> def f(x): return x + 1

    Simple composition of 2 functions

    >>> g = compose(f, f)
    >>> g(1)
    3

    Simple composition of 3 functions

    >>> g = compose(f, f, f)
    >>> g(1)
    4

    Also works with curried functions

    >>> def ff(x, y): return (x + 1) * y
    >>> f = curry(ff)

    >>> g = compose(f(1), f(2))
    >>> g(3) == f(2, f(1, 3))
    True
    >>> g(3)
    18

    >>> g = compose(f(y=1), f(y=2))
    >>> g(3)
    9

    """
    def f1(f, g):
        def f2(*arg, **kw):
            if arg:
                return f(g(*arg))
            else:
                return f(g(**kw))
        return f2

    def f3(*arg):
        return arg[0]

    def _compose(*functions):
        return functools.reduce(f1, functions, f3)

    return _compose(*reversed(functions))


def curry(func):
    """
    https://gist.github.com/JulienPalard/021f1c7332507d6a494b

    Decorator to curry a function, typical usage:
    >>> @curry
    ... def foo(a, b, c):
    ...    return a + b + c

    The function still work normally:

    >>> foo(1, 2, 3)
    6

    And in various curried forms:

    >>> foo(1)(2, 3)
    6
    >>> foo(1)(2)(3)
    6

    This also work with named arguments:

    >>> foo(a=1)(b=2)(c=3)
    6
    >>> foo(b=1)(c=2)(a=3)
    6
    >>> foo(a=1, b=2)(c=3)
    6
    >>> foo(a=1)(b=2, c=3)
    6

    And you may also change your mind on named arguments,
    But I don't know why you may want to do that:

    >>> foo(a=1, b=0)(b=2, c=3)
    6

    Finally, if you give more parameters than expected, the exception
    is the expected one, not some garbage produced by the currying
    mechanism:

    >>> foo(1, 2)(3, 4)
    Traceback (most recent call last):
       ...
    TypeError: foo() takes exactly 3 arguments (4 given)

    """
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return (lambda *args2, **kwargs2:
                curried(*(args + args2), **dict(kwargs, **kwargs2)))
    return curried


def cmd(command):

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
