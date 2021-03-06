from typing import Dict
from typing import Optional

def default_environment() -> Dict[str, str]: ...

class Marker:
    def __init__(self, marker: str) -> None: ...
    def evaluate(self, environment: Optional[Dict[str, str]] = ...) -> bool: ...

class InvalidMarker(ValueError): ...
class UndefinedComparison(ValueError): ...
class UndefinedEnvironmentName(ValueError): ...
