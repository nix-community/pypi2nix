from pypi2nix.license import license_from_string
from pypi2nix.logger import Logger
from pypi2nix.wheel import Wheel

from .logger import get_logger_output


def test_license_from_string_detects_apache_2_0() -> None:
    assert license_from_string("Apache 2.0") == "licenses.asl20"


def test_license_from_string_detects_bsd_dash_licenses() -> None:
    assert license_from_string("BSD - whatever") == "licenses.bsdOriginal"


def test_that_license_of_flit_is_detected(flit_wheel: Wheel, logger: Logger):
    assert flit_wheel.license
    assert "WARNING" not in get_logger_output(logger)
