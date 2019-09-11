import os
import os.path

from pypi2nix.pip.interface import Pip
from pypi2nix.requirement_set import RequirementSet

from ..switches import nix


@nix
def test_install_six_yields_non_empty_freeze_output(
    pip: Pip, project_dir, download_dir, current_platform, requirement_parser
):
    lib_dir = os.path.join(project_dir, "lib")
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_dir)
    pip.install(
        requirements, source_directories=[download_dir], target_directory=lib_dir
    )
    assert pip.freeze([lib_dir])


@nix
def test_install_to_target_directory_does_not_install_to_default_directory(
    pip: Pip, project_dir, download_dir, current_platform, requirement_parser
):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    target_directory = os.path.join(project_dir, "target-directory")
    os.makedirs(target_directory)
    pip.download_sources(requirements, download_dir)

    assert not os.listdir(target_directory)

    pip.install(
        requirements,
        source_directories=[download_dir],
        target_directory=target_directory,
    )

    assert os.listdir(target_directory)


@nix
def test_install_does_not_install_anything_with_empty_requirements(
    pip: Pip, project_dir, current_platform
):
    target_directory = os.path.join(project_dir, "target_dir")
    os.makedirs(target_directory)
    pip.install(RequirementSet(current_platform), [], target_directory)
    assert not os.listdir(target_directory)
