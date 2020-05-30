from typing import Dict
from typing import List
from typing import Tuple

from pypi2nix.package_source import PackageSource


class Sources:
    def __init__(self) -> None:
        self.sources: Dict[str, PackageSource] = dict()

    def add(self, name: str, source: PackageSource) -> None:
        self.sources[name] = source

    def __contains__(self, item: str) -> bool:
        return item in self.sources

    def __getitem__(self, item_name: str) -> PackageSource:
        return self.sources[item_name]

    def update(self, other_sources: "Sources") -> None:
        self.sources = dict(self.sources, **other_sources.sources)

    def items(self) -> List[Tuple[str, PackageSource]]:
        return list(self.sources.items())

    def __len__(self) -> int:
        return len(self.sources)
