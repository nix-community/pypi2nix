import operator
from enum import Enum
from enum import unique
from typing import Callable
from typing import Dict
from typing import Union

from attr import attrib
from attr import attrs
from packaging.version import InvalidVersion
from packaging.version import Version

from pypi2nix.target_platform import TargetPlatform

EnvironmentValue = Union["EnvironmentMarker", str, "MarkerToken"]
MarkerResult = bool


class MarkerEvaluationFailed(Exception):
    pass


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

    def evaluate(self, target_platform: TargetPlatform) -> str:
        if self is MarkerToken.EXTRA:
            return ""
        return getattr(target_platform, self.value)  # type: ignore


MARKERS_ENCODING_VERSION = {
    MarkerToken.PYTHON_VERSION,
    MarkerToken.PYTHON_FULL_VERSION,
    MarkerToken.IMPLEMENTATION_VERSION,
    MarkerToken.PLATFORM_VERSION,
}


@attrs
class EnvironmentMarker:
    """We implement PEP 508.
    Link to PEP 508: https://www.python.org/dev/peps/pep-0508/#environment-markers
    """

    _operation: str = attrib()
    left: EnvironmentValue = attrib()
    right: EnvironmentValue = attrib()

    def applies_to_platform(self, target_platform: TargetPlatform) -> bool:
        left = self._left_value(target_platform)
        right = self._right_value(target_platform)
        if isinstance(left, bool) and isinstance(right, bool):
            return self._bool_comparison(self._operation, left, right)
        if isinstance(left, Version) and isinstance(right, Version):
            return self._version_comparison(self._operation, left, right)
        if isinstance(left, str) and isinstance(right, str):
            return self._str_comparison(self._operation, left, right)
        raise MarkerEvaluationFailed(
            "Cannot handle marker values `{left}` and `{right}`".format(
                left=self.left, right=self.right
            )
        )

    def _left_value(self, target_platform: TargetPlatform) -> Union[str, bool, Version]:
        if isinstance(self.left, EnvironmentMarker):
            return self.left.applies_to_platform(target_platform)
        left: str
        if isinstance(self.left, MarkerToken):
            left = self.left.evaluate(target_platform)
        else:
            left = self.left
        if self._is_version_comparison():
            return _parse_version(left)
        else:
            return left

    def _right_value(
        self, target_platform: TargetPlatform
    ) -> Union[str, bool, Version]:
        if isinstance(self.right, EnvironmentMarker):
            return self.right.applies_to_platform(target_platform)
        right: str
        if isinstance(self.right, MarkerToken):
            right = self.right.evaluate(target_platform)
        else:
            right = self.right
        if self._is_version_comparison():
            return _parse_version(right)
        else:
            return right

    def _bool_comparison(self, symbol: str, left: bool, right: bool) -> bool:
        operations: Dict[str, Callable[[bool, bool], bool]] = {
            "and": lambda x, y: x and y,
            "or": lambda x, y: x or y,
        }
        try:
            operation = operations[symbol]
        except KeyError:
            raise MarkerEvaluationFailed(
                "Unknown operator for boolean values: {op}".format(op=symbol)
            )
        else:
            return operation(left, right)

    def _version_comparison(self, symbol: str, left: Version, right: Version) -> bool:
        operations: Dict[str, Callable[[Version, Version], bool]] = {
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
        }
        try:
            operation = operations[symbol]
        except KeyError:
            raise MarkerEvaluationFailed(
                "Unknown operator for Version values: {op}".format(op=symbol)
            )
        else:
            return operation(left, right)

    def _str_comparison(self, symbol: str, left: str, right: str) -> bool:
        operations: Dict[str, Callable[[str, str], bool]] = {
            "==": operator.eq,
            "!=": operator.ne,
            "in": lambda x, y: x in y,
            "not in": lambda x, y: x not in y,
        }
        try:
            operation = operations[symbol]
        except KeyError:
            raise MarkerEvaluationFailed(
                "Unknown operator for string values: {op}".format(op=symbol)
            )
        else:
            return operation(left, right)

    def _is_version_comparison(self) -> bool:
        return (
            self.left in MARKERS_ENCODING_VERSION
            or self.right in MARKERS_ENCODING_VERSION
        ) and self._operation not in ["in", "not in"]


def _parse_version(version: str) -> Version:
    try:
        return Version(version)
    except InvalidVersion:
        raise MarkerEvaluationFailed(
            "Cannot parse version {version_string}, legacy version format is not supported".format(
                version_string=version
            )
        )
