import json
import os
import shlex
import tempfile
from contextlib import contextmanager
from typing import Any
from typing import Dict
from typing import Iterator

from attr import attrib
from attr import attrs
from setuptools._vendor.packaging.markers import default_environment

from pypi2nix.nix import Nix
from pypi2nix.utils import PYTHON_VERSIONS


class PlatformGenerator:
    def __init__(self, nix: Nix) -> None:
        self.nix = nix

    def from_python_version(self, version: str) -> "TargetPlatform":
        python_command = ";".join(
            [
                "import json",
                "from setuptools._vendor.packaging.markers import default_environment",
                "print(json.dumps(default_environment()))",
            ]
        )
        with self._python_environment_nix(version) as nix_file:
            default_environment_string = self.nix.shell(
                command="python -c {command}".format(
                    command=shlex.quote(python_command)
                ),
                derivation_path=nix_file,
            )
        return self._target_platform_from_default_environment_string(
            default_environment_string,
            derivation_name=self._derivation_from_version_specifier(version),
        )

    def _target_platform_from_default_environment_string(
        self, json_string: str, derivation_name: str
    ) -> "TargetPlatform":
        default_environment = self._load_default_environment(json_string)
        return TargetPlatform(
            python_version=default_environment["python_version"],
            nixpkgs_derivation_name=derivation_name,
            python_full_version=default_environment["python_full_version"],
            implementation_version=default_environment["implementation_version"],
            os_name=default_environment["os_name"],
            implementation_name=default_environment["implementation_name"],
            sys_platform=default_environment["sys_platform"],
            platform_machine=default_environment["platform_machine"],
            platform_python_implementation=default_environment[
                "platform_python_implementation"
            ],
            platform_release=default_environment["platform_release"],
            platform_system=default_environment["platform_system"],
            platform_version=default_environment["platform_version"],
        )

    def _load_default_environment(self, json_string: str) -> Dict[str, str]:
        result: Dict[str, str] = dict()
        loaded_json = json.loads(json_string)
        if not isinstance(loaded_json, dict):
            return result
        for key, value in loaded_json.items():
            if isinstance(key, str) and isinstance(value, str):
                result[key] = value
        return result

    @contextmanager
    def _python_environment_nix(self, version: str) -> Iterator[str]:
        fd, path = tempfile.mkstemp()
        with open(fd, "w") as f:
            f.write(
                " ".join(
                    [
                        "with import <nixpkgs> {{}};",
                        "stdenv.mkDerivation {{",
                        'name = "python3-env";',
                        "buildInputs = with {interpreter}.pkgs; [{interpreter} {packages}];",
                        "}}",
                    ]
                ).format(
                    interpreter=self._derivation_from_version_specifier(version),
                    packages="setuptools",
                )
            )
        yield path
        os.remove(path)

    def _derivation_from_version_specifier(self, version: str) -> str:
        return PYTHON_VERSIONS[version]

    def current_platform(self) -> "TargetPlatform":
        environment_json_string = json.dumps(default_environment())
        environment = self._load_default_environment(environment_json_string)
        return self._target_platform_from_default_environment_string(
            environment_json_string,
            derivation_name=self._derivation_from_version_specifier(
                environment["python_version"]
            ),
        )


@attrs
class TargetPlatform:
    python_version: str = attrib()
    nixpkgs_derivation_name: str = attrib()
    python_full_version: str = attrib()
    implementation_version: str = attrib()
    os_name: str = attrib()
    sys_platform: str = attrib()
    implementation_name: str = attrib()
    platform_machine: str = attrib()
    platform_python_implementation: str = attrib()
    platform_release: str = attrib()
    platform_system: str = attrib()
    platform_version: str = attrib()

    def environment_dictionary(self) -> Dict[str, Any]:
        dictionary = {}
        dictionary["python_version"] = self.python_version
        dictionary["python_full_version"] = self.python_full_version
        dictionary["implementation_version"] = self.implementation_version
        dictionary["os_name"] = self.os_name
        dictionary["sys_platform"] = self.sys_platform
        dictionary["platform_machine"] = self.platform_machine
        dictionary[
            "platform_python_implementation"
        ] = self.platform_python_implementation
        dictionary["platform_release"] = self.platform_release
        dictionary["platform_system"] = self.platform_system
        dictionary["platform_version"] = self.platform_version
        dictionary["implementation_name"] = self.implementation_name
        return dictionary
