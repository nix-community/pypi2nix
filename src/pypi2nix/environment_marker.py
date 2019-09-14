from attr import attrib
from attr import attrs
from packaging.markers import InvalidMarker
from packaging.markers import Marker
from packaging.markers import UndefinedComparison
from packaging.markers import UndefinedEnvironmentName

from pypi2nix.target_platform import TargetPlatform


class MarkerEvaluationFailed(Exception):
    pass


@attrs
class EnvironmentMarker:
    _marker_string: str = attrib()

    def applies_to_platform(self, target_platform: TargetPlatform) -> bool:
        try:
            return Marker(self._marker_string).evaluate(
                target_platform.environment_dictionary()
            )
        except (InvalidMarker, UndefinedComparison, UndefinedEnvironmentName):
            raise MarkerEvaluationFailed(
                f"Failed to evaluate marker {self._marker_string}"
            )
