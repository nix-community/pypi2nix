import os
import os.path

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement

from ..switches import nix


def list_files(dirname):
    return [
        candidate
        for candidate in os.listdir(dirname)
        if os.path.isfile(os.path.join(dirname, candidate))
    ]


@nix
def test_pip_downloads_sources_to_target_directory(pip, project_dir):
    download_path = os.path.join(project_dir, "download")
    requirements = RequirementSet()
    requirements.add(Requirement.from_line("six"))
    pip.download_sources(requirements=requirements, target_directory=download_path)
    assert list_files(download_path)


@nix
def test_pip_downloads_nothing_when_no_requirements_are_given(pip, download_dir):
    pip.download_sources(requirements=RequirementSet(), target_directory=download_dir)
    assert not list_files(download_dir)
