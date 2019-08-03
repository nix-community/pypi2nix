from io import StringIO

import pytest

from pypi2nix.logger import Logger

from .logger import get_logger_output


@pytest.fixture
def logger():
    stream = StringIO("")
    logger = Logger(output=stream)
    return logger


def test_can_log_warning(logger: Logger):
    logger.warning("test")

    assert "WARNING: test" in get_logger_output(logger)


def test_every_line_of_warning_is_prefixed(logger):
    logger.warning("line1\nline2")

    output = get_logger_output(logger)
    assert "WARNING: line1" in output
    assert "WARNING: line2" in output


def test_can_log_error(logger: Logger):
    logger.error("test")

    assert "ERROR: test" in get_logger_output(logger)


def test_every_line_of_error_is_prefixed(logger: Logger):
    logger.error("line1\nline2")

    output = get_logger_output(logger)
    assert "ERROR: line1" in output
    assert "ERROR: line2" in output


def test_can_log_info(logger: Logger):
    logger.info("test")

    assert "INFO: test" in get_logger_output(logger)


def test_every_info_line_is_prefixed(logger: Logger):
    logger.info("line1\nline2")

    output = get_logger_output(logger)
    assert "INFO: line1" in output
    assert "INFO: line2" in output
