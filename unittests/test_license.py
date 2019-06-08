from pypi2nix.license import license_from_string


def test_license_from_string_detects_apache_2_0():
    assert license_from_string("Apache 2.0") == "licenses.asl20"


def test_license_from_string_detects_bsd_dash_licenses():
    assert license_from_string("BSD - whatever") == "licenses.bsdOriginal"
