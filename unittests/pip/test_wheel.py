from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from ..switches import nix


@nix
def test_pip_can_install_wheels_previously_downloaded(
    pip: Pip,
    project_dir: str,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
    download_dir: Path,
    wheels_dir: Path,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_dir)
    pip.build_wheels(
        requirements=requirements,
        source_directories=[download_dir],
        target_directory=wheels_dir,
    )
    assert wheels_dir.list_files()
    assert any(map(lambda x: x.endswith(".whl"), wheels_dir.list_files()))


@nix
def test_pip_wheel_does_not_build_wheels_if_requirements_are_empty(
    pip: Pip, wheels_dir: Path, download_dir: Path, current_platform: TargetPlatform
):
    pip.build_wheels(
        requirements=RequirementSet(current_platform),
        target_directory=wheels_dir,
        source_directories=[download_dir],
    )
    assert not wheels_dir.list_files()
