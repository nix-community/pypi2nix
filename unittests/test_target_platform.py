import json
import os
import os.path
import platform
import sys
from collections import namedtuple

import pytest
from packaging.markers import default_environment

from pypi2nix.environment_marker import EnvironmentMarker
from pypi2nix.python_version import PythonVersion
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.target_platform import TargetPlatform

from .switches import nix


def format_full_version(info):
    version = "{0.major}.{0.minor}.{0.micro}".format(info)
    kind = info.releaselevel
    if kind != "final":
        version += kind[0] + str(info.serial)
    return version


@pytest.fixture
def python_3_environment_nix(tmp_path_factory):
    directory = str(tmp_path_factory.mktemp("python_3_environment"))
    path = os.path.join(directory, "environment.nix")
    with open(path, "w") as f:
        f.write(
            " ".join(
                [
                    "with import <nixpkgs> {};",
                    'stdenv.mkDerivation { name = "python3-env"; buildInputs = [python3 python3.pkgs.setuptools]; }',
                ]
            )
        )
    return path


@pytest.fixture
def python_3_6_environment_nix(tmp_path_factory):
    directory = str(tmp_path_factory.mktemp("python_3_6_environment"))
    path = os.path.join(directory, "environment.nix")
    with open(path, "w") as f:
        f.write(
            " ".join(
                [
                    "with import <nixpkgs> {};",
                    'stdenv.mkDerivation { name = "python3-env"; buildInputs = [python36 python36.pkgs.setuptools]; }',
                ]
            )
        )
    return path


MarkerDefinition = namedtuple("NamedTuple", ["name", "value"])


@pytest.fixture(
    params=(
        MarkerDefinition("os_name", os.name),
        MarkerDefinition("sys_platform", sys.platform),
        MarkerDefinition("platform_machine", platform.machine()),
        MarkerDefinition(
            "platform_python_implementation", platform.python_implementation()
        ),
        MarkerDefinition("platform_release", platform.release()),
        MarkerDefinition("platform_system", platform.system()),
        MarkerDefinition("platform_version", platform.version()),
        MarkerDefinition(
            "python_version", ".".join(platform.python_version_tuple()[:2])
        ),
        MarkerDefinition("python_full_version", platform.python_version()),
        MarkerDefinition("implementation_name", sys.implementation.name),
        MarkerDefinition(
            "implementation_version",
            format_full_version(sys.implementation.version)
            if hasattr(sys, "implementation")
            else "0",
        ),
    )
)
def environment_marker_definition(request):
    """This fixture has been generate from https://www.python.org/dev/peps/pep-0508/#environment-markers"""
    return request.param


@nix
def test_that_target_platform_can_be_constructed_from_python_version(
    platform_generator: PlatformGenerator, nix, python_3_environment_nix
):
    platform = platform_generator.from_python_version(PythonVersion.python3)
    assert isinstance(platform, TargetPlatform)

    python_3_version = nix.shell(
        command='python -c "from platform import python_version; print(python_version()[:3])"',
        derivation_path=python_3_environment_nix,
    ).splitlines()[0]
    assert platform.python_version == python_3_version


@nix
def test_that_current_platform_to_environment_dict_equals_default_environment(
    current_platform: TargetPlatform
):
    assert current_platform.environment_dictionary() == default_environment()


@nix
def test_that_generated_platform_environment_dictionary_respects_python_version(
    platform_generator: PlatformGenerator, python_3_6_environment_nix, nix
):
    platform = platform_generator.from_python_version(PythonVersion.python36)
    assert isinstance(platform, TargetPlatform)
    output_string = nix.shell(
        command=" ".join(
            [
                'python -c "from setuptools._vendor.packaging.markers import default_environment;',
                "from json import dumps;",
                'print(dumps(default_environment()))"',
            ]
        ),
        derivation_path=python_3_6_environment_nix,
    )
    output_json = json.loads(output_string)
    assert platform.environment_dictionary() == output_json


def test_that_environment_marker_with_unknown_os_name_do_not_apply_to_current_platform(
    current_platform: TargetPlatform
):
    marker = EnvironmentMarker("os_name == 'fake_os_in_unittest'")
    assert not marker.applies_to_platform(current_platform)


def test_that_environment_markers_from_pep_are_correct_for_current_platform(
    environment_marker_definition: MarkerDefinition, current_platform: TargetPlatform
):
    assert (
        getattr(current_platform, environment_marker_definition.name)
        == environment_marker_definition.value
    )
