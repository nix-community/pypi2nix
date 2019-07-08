import os.path
import platform

import pytest

from pypi2nix.target_platform import PlatformGenerator

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
                    'stdenv.mkDerivation { name = "python3-env"; buildInputs = [python3]; }',
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
        command='python -c "from platform import python_version; print(python_version())"',
        derivation_path=python_3_environment_nix,
    ).splitlines()[0]
    assert platform.version == python_3_version


@nix
@pytest.mark.xfail
def test_that_target_platfrm_can_be_constructed_from_pypy(platform_generator):
    platform = platform_generator.from_python_version("pypy")
    assert platform.version == "pypy"


def test_that_we_can_generate_a_platform_from_the_current_environment(
    platform_generator
):
    current_platform = platform_generator.current_platform()
    assert current_platform.version == platform.python_version()
