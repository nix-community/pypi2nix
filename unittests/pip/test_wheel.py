import os.path
from typing import List

from pypi2nix.pip.interface import Pip
from pypi2nix.requirement_set import RequirementSet

from ..switches import nix


def list_files(dirname: str) -> List[str]:
    return [
        candidate
        for candidate in os.listdir(dirname)
        if os.path.isfile(os.path.join(dirname, candidate))
    ]


@nix
def test_pip_can_install_wheels_previously_downloaded(
    pip, project_dir, current_platform, requirement_parser
):
    download_directory = os.path.join(project_dir, "download")
    target_directory = os.path.join(project_dir, "wheels")
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_directory)
    pip.build_wheels(
        requirements=requirements,
        source_directories=[download_directory],
        target_directory=target_directory,
    )
    assert list_files(target_directory)
    assert any(map(lambda x: x.endswith(".whl"), list_files(target_directory)))


@nix
def test_pip_wheel_does_not_build_wheels_if_requirements_are_empty(
    pip: Pip, wheels_dir, download_dir, current_platform
):
    pip.build_wheels(
        requirements=RequirementSet(current_platform),
        target_directory=wheels_dir,
        source_directories=download_dir,
    )
    assert not list_files(wheels_dir)
