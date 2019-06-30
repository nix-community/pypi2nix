from pypi2nix.wheel import Wheel

from .switches import nix


@nix
def test_can_create_wheel_from_valid_directory(
    extracted_six_package, default_environment
):
    Wheel.from_wheel_directory_path(extracted_six_package, default_environment)
