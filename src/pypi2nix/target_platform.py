import os
import platform
import tempfile
from contextlib import contextmanager

from attr import attrib
from attr import attrs

from pypi2nix.utils import PYTHON_VERSIONS


class PlatformGenerator:
    def __init__(self, nix):
        self.nix = nix

    def from_python_version(self, version):
        with self.python_environment_nix(version) as nix_file:
            version = self.nix.shell(
                command='python -c "from platform import python_version; print(python_version())"',
                derivation_path=nix_file,
            ).splitlines()[0]
        return TargetPlatform(version)

    @contextmanager
    def python_environment_nix(self, version):
        fd, path = tempfile.mkstemp()
        with open(fd, "w") as f:
            f.write(
                " ".join(
                    [
                        "with import <nixpkgs> {{}};",
                        'stdenv.mkDerivation {{ name = "python3-env"; buildInputs = [{}]; }}',
                    ]
                ).format(self.derivation_from_version_specifier(version))
            )
        yield path
        os.remove(path)

    def derivation_from_version_specifier(self, version):
        return PYTHON_VERSIONS[version]

    def current_platform(self):
        return TargetPlatform(version=platform.python_version())


@attrs
class TargetPlatform:
    version = attrib()