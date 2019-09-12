import os.path

from pypi2nix.pip.interface import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from ..switches import nix


@nix
def test_freeze_on_empty_environment_yields_empty_file(pip: Pip):
    frozen_requirements = pip.freeze([])
    assert not frozen_requirements.strip()


@nix
def test_freeze_respects_additional_python_path(
    pip: Pip,
    project_dir: str,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
):
    prefix = os.path.join(project_dir, "custom-prefix")
    download_dir = os.path.join(project_dir, "download")
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_dir)
    pip.install(
        requirements, target_directory=prefix, source_directories=[download_dir]
    )
    freeze_without_six = pip.freeze([])
    freeze_with_six = pip.freeze(python_path=[prefix])
    assert len(freeze_without_six) < len(freeze_with_six)
