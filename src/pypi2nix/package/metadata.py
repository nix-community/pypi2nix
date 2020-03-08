import os
from email.header import Header
from email.parser import Parser as EmailParser

from attr import attrib
from attr import attrs

from .exceptions import DistributionNotDetected


@attrs
class PackageMetadata:
    name: str = attrib()

    @classmethod
    def from_package_directory(package_metadata, path: str) -> "PackageMetadata":
        builder = _PackageMetadataBuilder(path)
        return package_metadata(name=builder.name)


class _PackageMetadataBuilder:
    def __init__(self, path_to_directory: str) -> None:
        self.path_to_directory = path_to_directory
        self._name: str = ""

        self.build()

    @property
    def name(self) -> str:
        return self._name

    def build(self) -> None:
        pkg_info_file = os.path.join(self.path_to_directory, "PKG-INFO")
        try:
            with open(pkg_info_file) as f:
                parser = EmailParser()
                metadata = parser.parse(f)
        except FileNotFoundError:
            raise DistributionNotDetected(
                f"Could not find PKG-INFO file in {self.path_to_directory}"
            )
        self._name = metadata.get("name")
        if isinstance(self._name, Header):
            raise DistributionNotDetected(
                "Could not parse source distribution metadata, name detection failed"
            )
