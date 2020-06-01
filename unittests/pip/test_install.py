import os
import os.path

from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from ..switches import nix


@nix
def test_install_six_yields_non_empty_freeze_output(
    pip: Pip,
    project_dir: str,
    download_dir: Path,
    current_platform: TargetPlatform,
    requirement_parser,
):
    lib_dir = Path(os.path.join(project_dir, "lib"))
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_dir)
    pip.install(
        requirements, source_directories=[download_dir], target_directory=lib_dir
    )
    assert pip.freeze([lib_dir])


@nix
def test_install_to_target_directory_does_not_install_to_default_directory(
    pip: Pip,
    project_dir: str,
    download_dir: Path,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    target_directory = Path(project_dir) / "target-directory"
    target_directory.ensure_directory()
    pip.download_sources(requirements, download_dir)

    assert not target_directory.list_files()

    pip.install(
        requirements,
        source_directories=[download_dir],
        target_directory=target_directory,
    )

    assert target_directory.list_files()


@nix
def test_install_does_not_install_anything_with_empty_requirements(
    pip: Pip, project_dir: str, current_platform: TargetPlatform
):
    target_directory = Path(project_dir) / "target_dir"
    target_directory.ensure_directory()
    pip.install(RequirementSet(current_platform), [], target_directory)
    assert not target_directory.list_files()
