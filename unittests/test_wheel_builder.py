from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.target_platform import TargetPlatform

from .switches import nix


@nix
def test_extracts_myextra_dependencies_from_package3(
    wheel_builder: WheelBuilder,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    sources_for_test_packages: Sources,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("package3[myextra]"))
    wheel_paths = wheel_builder.build(requirements)
    stage2 = Stage2(sources_for_test_packages, logger, requirement_parser)
    wheels = stage2.main(
        wheel_paths, current_platform, wheel_builder.additional_build_dependencies
    )
    assert [wheel for wheel in wheels if wheel.name == "package1"]


@nix
def test_does_not_package_myextra_dependencies_if_no_extras_specified(
    wheel_builder: WheelBuilder,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    sources_for_test_packages: Sources,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("package3"))
    wheel_paths = wheel_builder.build(requirements)
    stage2 = Stage2(sources_for_test_packages, logger, requirement_parser)
    wheels = stage2.main(
        wheel_paths, current_platform, wheel_builder.additional_build_dependencies
    )
    assert not [wheel for wheel in wheels if wheel.name == "package1"]
