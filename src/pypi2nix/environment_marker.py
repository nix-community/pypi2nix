from enum import Enum
from enum import unique
from typing import Dict
from typing import Optional
from typing import Union

from attr import attrib
from attr import attrs

from pypi2nix.target_platform import TargetPlatform

EnvironmentValue = Union["EnvironmentMarker", str, "MarkerToken"]


@unique
class MarkerToken(Enum):
    PYTHON_VERSION = "python_version"
    PYTHON_FULL_VERSION = "python_full_version"
    IMPLEMENTATION_VERSION = "implementation_version"
    OS_NAME = "os_name"
    SYS_PLATFORM = "sys_platform"
    PLATFORM_MACHINE = "platform_machine"
    PLATFORM_PYTHON_IMPLEMENTATION = "platform_python_implementation"
    PLATFORM_RELEASE = "platform_release"
    PLATFORM_SYSTEM = "platform_system"
    PLATFORM_VERSION = "platform_version"
    IMPLEMENTATION_NAME = "implementation_name"
    EXTRA = "extra"

    @classmethod
    def get_from_string(token_class, token: str) -> "MarkerToken":
        mapping = {name.value: name for name in token_class}
        return mapping[token]


@attrs
class EnvironmentMarker:
    """We implement PEP 508.
    Link to PEP 508: https://www.python.org/dev/peps/pep-0508/#environment-markers
    """

    operation: str = attrib()
    left: EnvironmentValue = attrib()
    right: EnvironmentValue = attrib()

    def applies_to_platform(
        self, target_platform: TargetPlatform, extra: Optional[str] = None
    ) -> bool:
        mapping: Dict[MarkerToken, str] = {
            name: getattr(target_platform, name.value)
            for name in MarkerToken
            if name is not MarkerToken.EXTRA
        }

        def evaluate_marker(marker: EnvironmentValue) -> Union[str, bool, None]:
            if isinstance(marker, str):
                return marker
            elif isinstance(marker, MarkerToken):
                if marker is MarkerToken.EXTRA:
                    return extra
                return mapping[marker]
            else:
                operation = marker.operation
                left = evaluate_marker(marker.left)
                right = evaluate_marker(marker.right)
            if operation == "==":
                return left == right
            if operation == "!=":
                return left != right
            if isinstance(left, bool) and isinstance(right, bool):
                if operation == "or":
                    return left or right
                elif operation == "and":
                    return left and right
            elif isinstance(left, str) and isinstance(right, str):
                if operation == "in":
                    return left in right
                elif operation == "not in":
                    return left not in right
            raise Exception("Unknown operation: {}".format(operation))

        result = evaluate_marker(self)
        if isinstance(result, str):
            raise Exception("Expected bool here but found str {}.".format(result))
        elif result is None:
            raise Exception("Excpected bool here but found None.")
        else:
            return result
