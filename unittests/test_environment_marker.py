from pypi2nix.environment_marker import EnvironmentMarker
from pypi2nix.environment_marker import MarkerToken


def test_environment_marker_respects_supplied_extra(current_platform):
    marker = EnvironmentMarker(
        operation="==", left=MarkerToken.EXTRA, right="testextra"
    )
    assert marker.applies_to_platform(current_platform, extra="testextra")
    assert not marker.applies_to_platform(current_platform, extra=None)
