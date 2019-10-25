import json
import os.path
from collections import namedtuple
from contextlib import contextmanager
from typing import Dict
from typing import Iterator

from attr import attrib
from attr import attrs


@attrs
class Index:
    Entry = namedtuple("Entry", ["url", "sha256"])
    path: str = attrib()

    def __getitem__(self, key: str) -> "Index.Entry":
        with self._index_json() as index:
            return Index.Entry(url=index[key]["url"], sha256=index[key]["sha256"])

    def __setitem__(self, key: str, value: "Index.Entry") -> None:
        with self._index_json(write=True) as index:
            index[key] = {"url": value.url, "sha256": value.sha256}

    @contextmanager
    def _index_json(self, write: bool = False) -> Iterator[Dict[str, Dict[str, str]]]:
        with open(self.path) as f:
            index = json.load(f)
        yield index
        if write:
            with open(self.path, "w") as f:
                json.dump(index, f, sort_keys=True, indent=4)


INDEX = Index(os.path.join(os.path.dirname(__file__), "index.json"))
