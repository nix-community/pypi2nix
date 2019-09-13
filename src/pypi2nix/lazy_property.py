from functools import wraps
from typing import Callable
from typing import TypeVar

S = TypeVar("S")
T = TypeVar("T")


def lazy_property(method: Callable[[S], T]) -> property:
    @wraps(method)
    def wrapped_method(self: S) -> T:
        attribute_name = "_lazy_attribute_" + method.__name__
        if not hasattr(self, attribute_name):
            setattr(self, attribute_name, method(self))
        return getattr(self, attribute_name)  # type: ignore

    return property(wrapped_method)
