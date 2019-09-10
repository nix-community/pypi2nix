import json
import os.path
from contextlib import contextmanager
from typing import Dict
from typing import Iterator

from attr import attrib
from attr import attrs


@attrs
class Index:
    path: str = attrib()

    def absolute_path(self, key: str) -> str:
        file_name = self[key]
        return os.path.abspath(os.path.join(os.path.dirname(self.path), file_name))

    def __getitem__(self, key: str) -> str:
        with self._index_json() as index:
            return index[key]

    def __setitem__(self, key: str, value: str) -> None:
        with self._index_json(write=True) as index:
            index[key] = value

    @contextmanager
    def _index_json(self, write: bool = False) -> Iterator[Dict[str, str]]:
        with open(self.path) as f:
            index = json.load(f)
        yield index
        if write:
            with open(self.path, "w") as f:
                json.dump(index, f, sort_keys=True, indent=4)


INDEX = Index(os.path.join(os.path.dirname(__file__), "index.json"))


pip_wheel_path = INDEX["pip"]
