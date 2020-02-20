import pytest

from pypi2nix.python_version import PythonVersion
from pypi2nix.python_version import python_version_from_version_string
from pypi2nix.target_platform import PlatformGenerator

from .switches import nix


@pytest.mark.parametrize("python_version", PythonVersion)
@nix
def test_available_python_versions_exist_in_nixpkgs(
    python_version: PythonVersion, platform_generator: PlatformGenerator
):
    target_platform = platform_generator.from_python_version(python_version)
    assert target_platform is not None


@pytest.mark.parametrize(
    "version_string, expected_python_version",
    [
        ("3.5", PythonVersion.python35),
        ("3.6", PythonVersion.python36),
        ("3.7", PythonVersion.python37),
        ("3.8", PythonVersion.python38),
    ],
)
def test_can_get_python_version_from_version_string(
    version_string, expected_python_version
):
    assert python_version_from_version_string(version_string) == expected_python_version
