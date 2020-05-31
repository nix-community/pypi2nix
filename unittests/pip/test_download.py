import os
import os.path
from typing import List

from pypi2nix.path import Path
from pypi2nix.pip import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from ..switches import nix


def list_files(dirname: str) -> List[str]:
    return [
        candidate
        for candidate in os.listdir(dirname)
        if os.path.isfile(os.path.join(dirname, candidate))
    ]


@nix
def test_pip_downloads_sources_to_target_directory(
    pip: Pip,
    project_dir: str,
    current_platform: TargetPlatform,
    requirement_parser: RequirementParser,
):
    download_path = Path(project_dir) / "download"
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements=requirements, target_directory=download_path)
    assert download_path.list_files()


@nix
def test_pip_downloads_nothing_when_no_requirements_are_given(
    pip: Pip, download_dir: Path, current_platform: TargetPlatform
):
    pip.download_sources(
        requirements=RequirementSet(current_platform), target_directory=download_dir
    )
    assert not download_dir.list_files()
