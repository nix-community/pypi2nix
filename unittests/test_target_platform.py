import json
import os.path

import pytest
from setuptools._vendor.packaging.markers import default_environment

from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.target_platform import TargetPlatform

from .switches import nix


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


@pytest.fixture
def platform_generator(nix):
    return PlatformGenerator(nix=nix)


@nix
def test_that_target_platform_can_be_constructed_from_python_version(
    platform_generator, nix, python_3_environment_nix
):
    platform = platform_generator.from_python_version("3")

    python_3_version = nix.shell(
        command='python -c "from platform import python_version; print(python_version()[:3])"',
        derivation_path=python_3_environment_nix,
    ).splitlines()[0]
    assert platform.version == python_3_version


@nix
def test_that_current_platform_to_environment_dict_equals_default_environment(
    current_platform: TargetPlatform
):
    assert current_platform.environment_dictionary() == default_environment()


@nix
def test_that_generated_platform_environment_dictionary_respects_python_version(
    platform_generator, python_3_6_environment_nix, nix
):
    platform = platform_generator.from_python_version("3.6")
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
