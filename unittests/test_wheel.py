import json

import pytest

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.wheel import Wheel

from .switches import nix


@pytest.fixture
def wheel(current_platform):
    build_dependencies = RequirementSet(current_platform)
    dependencies = RequirementSet(current_platform)
    return Wheel(
        name="test-wheel",
        version="1.0",
        deps=dependencies,
        homepage="https://example.test",
        license="",
        description="description",
        build_dependencies=build_dependencies,
    )


@nix
def test_can_create_wheel_from_valid_directory(
    extracted_six_package, current_platform, logger, requirement_parser
):
    Wheel.from_wheel_directory_path(
        extracted_six_package, current_platform, logger, requirement_parser
    )


@nix
def test_can_add_build_dependencies_to_wheel(
    wheel, current_platform, requirement_parser
):
    build_dependencies = RequirementSet(current_platform)
    build_dependencies.add(requirement_parser.parse("dep1"))
    build_dependencies.add(requirement_parser.parse("dep2"))
    wheel.add_build_dependencies(build_dependencies)
    build_dependency_names = [x.name() for x in wheel.build_dependencies]
    assert "dep1" in build_dependency_names
    assert "dep2" in build_dependency_names


def test_that_to_dict_is_json_serializable(wheel):
    json.dumps(wheel.to_dict())
