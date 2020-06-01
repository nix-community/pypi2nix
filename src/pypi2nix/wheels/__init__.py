import json
import os.path
from collections import namedtuple
from contextlib import contextmanager
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Union

from attr import attrib
from attr import attrs
from jsonschema import ValidationError
from jsonschema import validate

from pypi2nix.logger import Logger
from pypi2nix.path import Path

from .schema import GIT_SCHEMA
from .schema import INDEX_SCHEMA
from .schema import URL_SCHEMA


@attrs
class Index:
    UrlEntry = namedtuple("UrlEntry", ["url", "sha256"])
    GitEntry = namedtuple("GitEntry", ["url", "sha256", "rev"])
    Entry = Union[UrlEntry, GitEntry]

    logger: Logger = attrib()
    path: Path = attrib(default=Path(os.path.dirname(__file__)) / "index.json",)

    def __getitem__(self, key: str) -> "Index.Entry":
        with self._index_json() as index:
            entry = index[key]
            if self._is_schema_valid(entry, URL_SCHEMA):
                return Index.UrlEntry(url=entry["url"], sha256=entry["sha256"])
            elif self._is_schema_valid(entry, GIT_SCHEMA):
                return Index.GitEntry(
                    url=entry["url"], sha256=entry["sha256"], rev=entry["rev"]
                )
            else:
                raise Exception()

    def __setitem__(self, key: str, value: "Index.Entry") -> None:
        with self._index_json(write=True) as index:
            if isinstance(value, self.UrlEntry):
                index[key] = {
                    "url": value.url,
                    "sha256": value.sha256,
                    "__type__": "fetchurl",
                }
            if isinstance(value, self.GitEntry):
                index[key] = {
                    "url": value.url,
                    "sha256": value.sha256,
                    "rev": value.rev,
                    "__type__": "fetchgit",
                }

    def is_valid(self) -> bool:
        with self._index_json() as index:
            return self._is_schema_valid(index, INDEX_SCHEMA)

    @contextmanager
    def _index_json(self, write: bool = False) -> Iterator[Dict[str, Dict[str, str]]]:
        with open(str(self.path)) as f:
            index = json.load(f)
        yield index
        if write:
            with open(str(self.path), "w") as f:
                json.dump(index, f, sort_keys=True, indent=4)

    def _is_schema_valid(self, json_value: Any, schema: Any) -> bool:
        try:
            validate(json_value, schema)
        except ValidationError as e:
            self.logger.error(str(e))
            return False
        else:
            return True
