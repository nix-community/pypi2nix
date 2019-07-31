from enum import Enum
from enum import unique
from typing import Dict
from typing import Union

from attr import attrib
from attr import attrs

from pypi2nix.target_platform import TargetPlatform

EnvironmentValue = Union["EnvironmentMarker", str, "MarkerToken"]


@unique
class MarkerToken(Enum):
    PYTHON_VERSION = 1


@attrs
class EnvironmentMarker:
    operation: str = attrib()
    left: EnvironmentValue = attrib()
    right: EnvironmentValue = attrib()

    def applies_to_platform(self, target_platform: TargetPlatform) -> bool:
        mapping: Dict[MarkerToken, str] = {
            MarkerToken.PYTHON_VERSION: ".".join(target_platform.version.split(".")[:2])
        }

        def evaluate_marker(marker: EnvironmentValue) -> Union[str, bool]:
            if isinstance(marker, str):
                return marker
            elif isinstance(marker, MarkerToken):
                return mapping[marker]
            else:
                operation = marker.operation
                left = evaluate_marker(marker.left)
                right = evaluate_marker(marker.right)
            if isinstance(left, bool) and isinstance(right, bool):
                if operation == "or":
                    return left or right
                elif operation == "and":
                    return left and right
                elif operation == "==":
                    return left == right
                elif operation == "!=":
                    return left != right
            elif isinstance(left, str) and isinstance(right, str):
                if operation == "in":
                    return left in right
                elif operation == "not in":
                    return left not in right
                elif operation == "==":
                    return left == right
                elif operation == "!=":
                    return left != right
            raise Exception("Unknown operation: {}".format(operation))

        result = evaluate_marker(self)
        if isinstance(result, str):
            raise Exception("Expected bool here but found str {}".format(result))
        else:
            return result
