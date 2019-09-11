from io import StringIO

import pytest

from pypi2nix.logger import Logger
from pypi2nix.logger import LoggerNotConnected
from pypi2nix.logger import ProxyLogger
from pypi2nix.logger import StreamLogger
from pypi2nix.logger import Verbosity
from pypi2nix.logger import verbosity_from_int

from .logger import get_logger_output


@pytest.fixture(params=["proxy", "stream"])
def logger(request):
    stream = StringIO("")
    stream_logger = StreamLogger(output=stream)
    if request.param == "stream":
        return stream_logger
    elif request.param == "proxy":
        proxy_logger = ProxyLogger()
        proxy_logger.set_target_logger(stream_logger)
        return proxy_logger


@pytest.fixture
def unconnected_proxy_logger():
    return ProxyLogger()


def test_can_log_warning(logger: Logger):
    logger.warning("test")

    assert "WARNING: test" in get_logger_output(logger)


def test_every_line_of_warning_is_prefixed(logger):
    logger.warning("line1\nline2")

    output = get_logger_output(logger)
    assert "WARNING: line1" in output
    assert "WARNING: line2" in output


@pytest.mark.parametrize("level", (Verbosity.ERROR,))
def test_that_logger_with_low_verbosity_level_does_not_emit_warning_logs(
    logger: Logger, level
):
    logger.set_verbosity(level)
    logger.warning("test")

    output = get_logger_output(logger)
    assert "WARNING" not in output


@pytest.mark.parametrize("level", (Verbosity.WARNING, Verbosity.INFO, Verbosity.DEBUG))
def test_that_logger_with_high_verbosity_level_does_emit_warning_logs(
    logger: Logger, level: Verbosity
):
    logger.set_verbosity(level)
    logger.warning("test")

    output = get_logger_output(logger)
    assert "WARNING" in output


def test_can_log_error(logger: Logger):
    logger.error("test")

    assert "ERROR: test" in get_logger_output(logger)


def test_every_line_of_error_is_prefixed(logger: Logger):
    logger.error("line1\nline2")

    output = get_logger_output(logger)
    assert "ERROR: line1" in output
    assert "ERROR: line2" in output


@pytest.mark.parametrize(
    "level", (Verbosity.ERROR, Verbosity.WARNING, Verbosity.INFO, Verbosity.DEBUG)
)
def test_that_logger_always_emits_errors(logger: Logger, level: Verbosity):
    logger.set_verbosity(level)
    logger.error("test")

    output = get_logger_output(logger)
    assert "ERROR" in output


def test_can_log_info(logger: Logger):
    logger.info("test")

    assert "INFO: test" in get_logger_output(logger)


def test_every_info_line_is_prefixed(logger: Logger):
    logger.info("line1\nline2")

    output = get_logger_output(logger)
    assert "INFO: line1" in output
    assert "INFO: line2" in output


@pytest.mark.parametrize("level", (Verbosity.WARNING, Verbosity.ERROR))
def test_that_logger_with_low_verbosity_level_does_not_emit_info_logs(
    logger: Logger, level
):
    logger.set_verbosity(level)
    logger.info("test")

    output = get_logger_output(logger)
    assert "INFO" not in output


@pytest.mark.parametrize("level", (Verbosity.INFO, Verbosity.DEBUG))
def test_that_logger_with_high_verbosity_level_does_emit_info_logs(
    logger: Logger, level: Verbosity
):
    logger.set_verbosity(level)
    logger.info("test")

    output = get_logger_output(logger)
    assert "INFO" in output


def test_can_log_debug(logger: Logger):
    logger.debug("test")

    assert "DEBUG: test" in get_logger_output(logger)


def test_every_debug_line_is_prefixed(logger: Logger):
    logger.debug("line1\nline2")

    output = get_logger_output(logger)
    assert "DEBUG: line1" in output
    assert "DEBUG: line2" in output


@pytest.mark.parametrize("level", (Verbosity.WARNING, Verbosity.ERROR, Verbosity.INFO))
def test_that_logger_with_low_verbosity_level_does_not_emit_debug_logs(
    logger: Logger, level
):
    logger.set_verbosity(level)
    logger.debug("test")

    output = get_logger_output(logger)
    assert "DEBUG" not in output


@pytest.mark.parametrize("level", (Verbosity.DEBUG,))
def test_that_logger_with_high_verbosity_level_does_emit_debug_logs(
    logger: Logger, level: Verbosity
):
    logger.set_verbosity(level)
    logger.debug("test")

    output = get_logger_output(logger)
    assert "DEBUG" in output


@pytest.mark.parametrize("level", list(Verbosity))
def test_that_verbosity_level_can_be_retrieved_from_assigned_integer(level):
    assert verbosity_from_int(level.value) == level


def test_that_high_number_gets_translated_into_debug_verbosity():
    assert verbosity_from_int(10000) == Verbosity.DEBUG


def test_that_low_number_gets_translated_into_error_verbosity():
    assert verbosity_from_int(-10000) == Verbosity.ERROR


def test_that_unconnect_proxy_logger_raises_proper_exception_on_logging(
    unconnected_proxy_logger
):
    with pytest.raises(LoggerNotConnected):
        unconnected_proxy_logger.debug("test")
    with pytest.raises(LoggerNotConnected):
        unconnected_proxy_logger.info("test")
    with pytest.raises(LoggerNotConnected):
        unconnected_proxy_logger.warning("test")
    with pytest.raises(LoggerNotConnected):
        unconnected_proxy_logger.error("test")
    with pytest.raises(LoggerNotConnected):
        unconnected_proxy_logger.set_verbosity(Verbosity.DEBUG)
