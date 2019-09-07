import pytest

from pypi2nix.environment_marker import EnvironmentMarker
from pypi2nix.environment_marker import MarkerToken


@pytest.mark.parametrize("operator", ("<", "<=", "==", "!=", ">", ">="))
def test_that_version_comparisons_do_not_throw(operator, current_platform):
    marker = EnvironmentMarker(
        operation=operator, left="1.0", right=MarkerToken.PYTHON_VERSION
    )
    marker.applies_to_platform(current_platform)
