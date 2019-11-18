import email
import os
from email.header import Header

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
        extracted_files = [
            os.path.join(directory_path, file_name)
            for directory_path, _, file_names in os.walk(self.path_to_directory)
            for file_name in file_names
        ]
        pkg_info_files = [
            filepath for filepath in extracted_files if filepath.endswith("PKG-INFO")
        ]
        if not pkg_info_files:
            raise DistributionNotDetected(
                "`{}` does not appear to be a python source distribution, Could not find PKG-INFO file".format(
                    self.path_to_directory
                )
            )
        pkg_info_file = pkg_info_files[0]
        with open(pkg_info_file) as f:
            metadata = email.parser.Parser().parse(f)
        self._name = metadata.get("name")
        if isinstance(self._name, Header):
            raise DistributionNotDetected(
                "Could not parse source distribution metadata, name detection failed"
            )
