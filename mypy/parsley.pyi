from typing import Any
from typing import Callable
from typing import Dict
from typing import overload

class ParseError(Exception):
    def formatError(self) -> str: ...

@overload
def makeGrammar(source: str, bindings: Dict[str, Callable[..., Any]]) -> Any: ...
@overload
def makeGrammar(
    source: str, bindings: Dict[str, Callable[..., Any]], name: str
) -> Any: ...
@overload
def makeGrammar(
    source: str, bindings: Dict[str, Callable[..., Any]], unwrap: bool
) -> Any: ...
@overload
def makeGrammar(
    source: str, bindings: Dict[str, Callable[..., Any]], name: str, unwrap: bool
) -> Any: ...
