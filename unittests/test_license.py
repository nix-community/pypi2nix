from pypi2nix.license import license_from_string

from .logger import get_logger_output


def test_license_from_string_detects_apache_2_0():
    assert license_from_string("Apache 2.0") == "licenses.asl20"


def test_license_from_string_detects_bsd_dash_licenses():
    assert license_from_string("BSD - whatever") == "licenses.bsdOriginal"


def test_that_license_of_flit_is_detected(flit_wheel, logger):
    assert flit_wheel.license
    assert "WARNING" not in get_logger_output(logger)
