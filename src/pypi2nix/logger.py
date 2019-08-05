from enum import Enum
from enum import unique
from typing import TextIO


@unique
class Verbosity(Enum):
    ERROR = -1
    WARNING = 0
    INFO = 1
    DEBUG = 2


VERBOSITY_MIN: int = min(*map(lambda v: v.value, Verbosity))  # type: ignore
VERBOSITY_MAX: int = max(*map(lambda v: v.value, Verbosity))  # type: ignore


def verbosity_from_int(n: int) -> Verbosity:
    for verbosity_level in Verbosity:
        if verbosity_level.value == n:
            return verbosity_level
    if n < VERBOSITY_MIN:
        return Verbosity.ERROR
    else:
        return Verbosity.DEBUG


class Logger:
    def __init__(self, output: TextIO):
        self.output = output
        self.verbosity_level: Verbosity = Verbosity.DEBUG

    def warning(self, text: str) -> None:
        if self.verbosity_level.value >= Verbosity.WARNING.value:
            for line in text.splitlines():
                print("WARNING:", line, file=self.output)

    def error(self, text: str) -> None:
        for line in text.splitlines():
            print("ERROR:", line, file=self.output)

    def info(self, text: str) -> None:
        if self.verbosity_level.value >= Verbosity.INFO.value:
            for line in text.splitlines():
                print("INFO:", line, file=self.output)

    def debug(self, text: str) -> None:
        if self.verbosity_level.value >= Verbosity.DEBUG.value:
            for line in text.splitlines():
                print("DEBUG:", line, file=self.output)

    def set_verbosity(self, level: Verbosity) -> None:
        self.verbosity_level = level
