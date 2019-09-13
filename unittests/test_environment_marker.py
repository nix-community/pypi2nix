import pytest

from pypi2nix.environment_marker import EnvironmentMarker


@pytest.mark.parametrize("operator", ("<", "<=", "==", "!=", ">", ">="))
def test_that_version_comparisons_do_not_throw(operator, current_platform):
    marker = EnvironmentMarker(f"python_version {operator} '1.0'")
    marker.applies_to_platform(current_platform)
