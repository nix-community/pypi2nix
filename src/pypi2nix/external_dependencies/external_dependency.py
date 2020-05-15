from attr import attrib
from attr import attrs


@attrs(frozen=True)
class ExternalDependency:
    _attribute_name: str = attrib()

    def attribute_name(self) -> str:
        return self._attribute_name
