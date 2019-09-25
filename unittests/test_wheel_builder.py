from typing import List

import pytest

from pypi2nix.logger import Logger
from pypi2nix.pypi import Pypi
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.target_platform import TargetPlatform
from pypi2nix.wheel import Wheel

from .switches import nix


@pytest.fixture
def build_wheels(
    wheel_builder: WheelBuilder,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    sources_for_test_packages: Sources,
    pypi: Pypi,
):
    def wrapper(requirement_lines: List[str]) -> List[Wheel]:
        requirements = RequirementSet(current_platform)
        for line in requirement_lines:
            requirements.add(requirement_parser.parse(line))
        wheel_paths = wheel_builder.build(requirements)
        stage2 = Stage2(sources_for_test_packages, logger, requirement_parser, pypi)
        return stage2.main(
            wheel_paths, current_platform, wheel_builder.additional_build_dependencies
        )

    return wrapper


@nix
def test_extracts_myextra_dependencies_from_package3(build_wheels,):
    wheels = build_wheels(["package3[myextra]"])
    assert [wheel for wheel in wheels if wheel.name == "package1"]


@nix
def test_does_not_package_myextra_dependencies_if_no_extras_specified(build_wheels,):
    wheels = build_wheels(["package3"])
    assert not [wheel for wheel in wheels if wheel.name == "package1"]


@nix
def test_does_detect_extra_requirements_from_requirements(build_wheels):
    wheels = build_wheels(["package4"])
    assert [wheel for wheel in wheels if wheel.name == "package1"]


@nix
def test_that_we_filter_extra_requirements_that_do_not_apply_to_target_platform(
    build_wheels,
):
    wheels = build_wheels(["package3[other_platform]"])
    assert not [wheel for wheel in wheels if wheel.name == "package2"]
