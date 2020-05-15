from __future__ import annotations

import sys
from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from enum import unique
from typing import Optional
from typing import TextIO


class LoggerNotConnected(Exception):
    pass


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


class Logger(metaclass=ABCMeta):
    @abstractmethod
    def error(self, text: str) -> None:
        pass

    @abstractmethod
    def warning(self, text: str) -> None:
        pass

    @abstractmethod
    def info(self, text: str) -> None:
        pass

    @abstractmethod
    def debug(self, text: str) -> None:
        pass

    @abstractmethod
    def set_verbosity(self, level: Verbosity) -> None:
        pass


class StreamLogger(Logger):
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

    @classmethod
    def stdout_logger(constructor) -> StreamLogger:
        return constructor(sys.stdout)


class ProxyLogger(Logger):
    def __init__(self) -> None:
        self._target_logger: Optional[Logger] = None

    def info(self, text: str) -> None:
        if self._target_logger is not None:
            self._target_logger.info(text)
        else:
            raise LoggerNotConnected("Logger not connected")

    def debug(self, text: str) -> None:
        if self._target_logger is not None:
            self._target_logger.debug(text)
        else:
            raise LoggerNotConnected("Logger not connected")

    def warning(self, text: str) -> None:
        if self._target_logger is not None:
            self._target_logger.warning(text)
        else:
            raise LoggerNotConnected("Logger not connected")

    def error(self, text: str) -> None:
        if self._target_logger is not None:
            self._target_logger.error(text)
        else:
            raise LoggerNotConnected("Logger not connected")

    def set_verbosity(self, level: Verbosity) -> None:
        if self._target_logger is not None:
            self._target_logger.set_verbosity(level)
        else:
            raise LoggerNotConnected("Logger not connected")

    def set_target_logger(self, target: Logger) -> None:
        self._target_logger = target

    def get_target_logger(self) -> Optional[Logger]:
        return self._target_logger
