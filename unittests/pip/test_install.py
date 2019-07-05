import os
import os.path

from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement

from ..switches import nix


@nix
def test_install_six_yields_non_empty_freeze_output(pip, project_dir, download_dir):
    requirements = RequirementSet()
    requirements.add(Requirement.from_line("six"))
    pip.download_sources(requirements, download_dir)
    pip.install(requirements, source_directories=[download_dir])
    assert pip.freeze()


@nix
def test_install_to_target_directory_does_not_install_to_default_directory(
    pip, project_dir, download_dir
):
    requirements = RequirementSet()
    requirements.add(Requirement.from_line("six"))
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
def test_install_does_not_install_anything_with_empty_requirements(pip, project_dir):
    target_directory = os.path.join(project_dir, "target_dir")
    os.makedirs(target_directory)
    pip.install([], [], target_directory)
    assert not os.listdir(target_directory)
