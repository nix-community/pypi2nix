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
def test_pip_can_install_wheels_previously_downloaded(pip, project_dir):
    download_directory = os.path.join(project_dir, "download")
    target_directory = os.path.join(project_dir, "wheels")
    requirements = [RequirementsFile.from_lines(["six"], project_dir)]
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
    pip, wheels_dir, download_dir
):
    pip.build_wheels(
        requirements=[], target_directory=wheels_dir, source_directories=download_dir
    )
    assert not list_files(wheels_dir)
