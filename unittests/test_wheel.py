import pytest

from pypi2nix.wheel import Wheel

from .switches import nix


@pytest.fixture
def wheel():
    return Wheel(
        name="test-wheel",
        version="1.0",
        deps=set(),
        homepage="https://example.test",
        license=None,
        description="description",
    )


@nix
def test_can_create_wheel_from_valid_directory(
    extracted_six_package, default_environment
):
    Wheel.from_wheel_directory_path(extracted_six_package, default_environment)


@nix
def test_can_add_build_dependencies_to_wheel(wheel):
    wheel.add_build_dependencies(["dep1", "dep2"])
    assert "dep1" in wheel.build_dependencies
    assert "dep2" in wheel.build_dependencies
