import os
import os.path

import pytest

from pypi2nix.requirements_file import RequirementsFile

from ..switches import nix


@pytest.fixture
def download_dir(project_dir):
    return os.path.join(project_dir, "download")


@nix
def test_install_six_yields_non_empty_freeze_output(pip, project_dir, download_dir):
    requirements = [RequirementsFile.from_lines(["six"], project_dir)]
    pip.download_sources(requirements, download_dir)
    pip.install(requirements, source_directories=[download_dir])
    assert pip.freeze()


@nix
def test_install_to_target_directory_does_not_install_to_default_directory(
    pip, project_dir, download_dir
):
    requirements = [RequirementsFile.from_lines(["six"], project_dir)]
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
