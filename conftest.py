import os
import os.path
import platform

import pytest
from pypi2nix.nix import Nix
from pypi2nix.pip import Pip
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.stage1 import WheelBuilder


@pytest.fixture
def python_version():
    return '.'.join(
        platform.python_version().split('.')[:2]
    )


@pytest.fixture
def nix():
    return Nix(verbose=True)


@pytest.fixture
def project_dir(tmpdir):
    return str(tmpdir)


@pytest.fixture
def download_dir(project_dir):
    path = os.path.join(project_dir, 'download')
    os.makedirs(path)
    return path


@pytest.fixture
def wheels_dir(project_dir):
    path = os.path.join(project_dir, 'wheels')
    os.makedirs(path)
    return path


@pytest.fixture
def pip(nix, project_dir):
    return Pip(
        nix=nix,
        project_directory=project_dir,
        extra_build_inputs=[],
        python_version="python3",
        extra_env="",
        verbose=3,
        wheels_cache=[],
    )


@pytest.fixture
def wheel_builder(pip, project_dir):
    return WheelBuilder(pip, project_dir)


@pytest.fixture
def extracted_six_package(six_requirements, wheel_builder):
    wheels = wheel_builder.build(six_requirements)
    assert len(wheels) == 1
    return wheels[0]


@pytest.fixture
def six_requirements(project_dir):
    requirements = RequirementSet()
    requirements.add(Requirement.from_line('six'))
    return requirements


@pytest.fixture
def default_environment(pip):
    return pip.default_environment()


@pytest.fixture
def six_source_distribution(pip, download_dir, six_requirements):
    pip.download_sources(
        six_requirements,
        download_dir,
    )
    for file_name in os.listdir(download_dir):
        if 'six' in file_name:
            return os.path.join(download_dir, file_name)
