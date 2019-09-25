import pytest

from pypi2nix.logger import Logger
from pypi2nix.pypi import Pypi

from .switches import nix


@pytest.fixture
def pypi(logger: Logger):
    return Pypi(logger)


@nix
def test_pypi_get_package_returns_package_with_correct_name(pypi):
    assert pypi.get_package("six").name == "six"


@nix
def test_pypi_get_package_returns_package_with_releases(pypi):
    assert pypi.get_package("six").releases


@nix
def test_pypi_gets_correct_source_release_for_package_version_with_only_source_release(
    pypi
):
    release = pypi.get_source_release("six", "0.9.0")
    assert (
        release.sha256_digest
        == "14fd1ed3dd0e1a46cc53b8fc890b5a3b11737515aeb7f42c3af9f38e8d8975d7"
    )


@nix
def test_pypi_gets_correct_source_release_for_package_with_multiple_release_types(pypi):
    release = pypi.get_source_release("six", "1.12.0")
    assert (
        release.sha256_digest
        == "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73"
    )


@nix
def test_pypi_gets_correct_source_release_for_radiotherm_1_2(pypi):
    release = pypi.get_source_release("radiotherm", "1.2")
    assert (
        release.sha256_digest
        == "e8a70e0cf38f21170a3a43d5de62954aa38032dfff20adcdf79dd6c39734b8cc"
    )


@nix
def test_pypi_gets_correct_source_release_for_setuptools_1_6_0(pypi):
    release = pypi.get_source_release("setuptools-scm", "1.6.0")
    assert (
        release.sha256_digest
        == "c4f1b14e4fcc7dd69287a6c0b571c889dd4970559c7fa0512b2311f1513d86f4"
    )
