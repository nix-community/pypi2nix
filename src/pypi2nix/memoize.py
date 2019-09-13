from functools import wraps
from typing import Callable
from typing import TypeVar

S = TypeVar("S")
T = TypeVar("T")


def memoize(method: Callable[[S], T]) -> Callable[[S], T]:
    @wraps(method)
    def wrapped_method(self: S) -> T:
        attribute_name = "_memoize_attribute_" + method.__name__
        if not hasattr(self, attribute_name):
            setattr(self, attribute_name, method(self))
        return getattr(self, attribute_name)  # type: ignore

    return wrapped_method
