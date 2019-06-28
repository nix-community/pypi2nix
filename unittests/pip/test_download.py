import os
import os.path

from pypi2nix.requirements_file import RequirementsFile

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
    pip.download_sources(
        requirements=[RequirementsFile.from_lines(["six"], project_dir=project_dir)],
        constraints=[],
        target_directory=download_path,
    )
    assert list_files(download_path)
