import os.path

from pypi2nix.logger import Logger
from pypi2nix.package_source import PathSource
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.stage2 import Stage2
from pypi2nix.target_platform import TargetPlatform

from .switches import nix


@nix
def test_extracts_testing_dependencies_from_setupcfg_package(
    wheel_builder: WheelBuilder,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    data_directory: str,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("setupcfg-package[testing]"))
    wheel_paths = wheel_builder.build(requirements)
    sources = Sources()
    sources.add(
        "setupcfg-package",
        PathSource(
            os.path.join(data_directory, "setupcfg-package", "setupcfg-package.tar.gz")
        ),
    )
    stage2 = Stage2(sources, logger, requirement_parser)
    wheels = stage2.main(
        wheel_paths, current_platform, wheel_builder.additional_build_dependencies
    )
    for wheel in wheels:
        if wheel.name == 'pytest':
            assert True
    else:
        assert False


@nix
def test_does_not_package_testing_dependencies_if_no_extras_specified(
    wheel_builder: WheelBuilder,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    logger: Logger,
    data_directory: str,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("setupcfg-package"))
    wheel_paths = wheel_builder.build(requirements)
    sources = Sources()
    sources.add(
        "setupcfg-package",
        PathSource(
            os.path.join(data_directory, "setupcfg-package", "setupcfg-package.tar.gz")
        ),
    )
    stage2 = Stage2(sources, logger, requirement_parser)
    wheels = stage2.main(
        wheel_paths, current_platform, wheel_builder.additional_build_dependencies
    )
    for wheel in wheels:
        if wheel.name == 'pytest':
            assert False
    else:
        assert True
