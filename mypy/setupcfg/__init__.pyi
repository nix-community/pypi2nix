from typing import overload

from setupcfg.cfg import Setupcfg
@overload
def load() -> Setupcfg: ...
@overload
def load(path: str) -> Setupcfg: ...
