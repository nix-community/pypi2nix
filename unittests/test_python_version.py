import pytest

from pypi2nix.python_version import PythonVersion
from pypi2nix.target_platform import PlatformGenerator

from .switches import nix


@pytest.mark.parametrize("python_version", PythonVersion)
@nix
def test_available_python_versions_exist_in_nixpkgs(
    python_version: PythonVersion, platform_generator: PlatformGenerator
):
    target_platform = platform_generator.from_python_version(python_version)
    assert target_platform is not None
