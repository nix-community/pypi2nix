import os.path

from pypi2nix.requirements_file import RequirementsFile


def test_install_six_yields_non_empty_freeze_output(pip, project_dir):
    download_dir = os.path.join(project_dir, "download")
    requirements = [RequirementsFile.from_lines(["six"], project_dir)]
    pip.download_sources(requirements, download_dir)
    pip.install(requirements, source_directories=[download_dir])
    assert pip.freeze()
