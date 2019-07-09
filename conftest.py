import os
import os.path
import platform

import pytest
from pypi2nix.archive import Archive
from pypi2nix.nix import Nix
from pypi2nix.pip import Pip
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.target_platform import PlatformGenerator

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "unittests", "data")


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
def pip(nix, project_dir, current_platform):
    return Pip(
        nix=nix,
        project_directory=project_dir,
        extra_build_inputs=[],
        python_version="python3",
        extra_env="",
        verbose=3,
        wheels_cache=[],
        target_platform=current_platform,
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
def six_source_distribution_archive(pip, download_dir, six_requirements):
    pip.download_sources(
        six_requirements,
        download_dir,
    )
    for file_name in os.listdir(download_dir):
        if 'six' in file_name:
            return Archive(path=os.path.join(download_dir, file_name))


@pytest.fixture
def requirements_for_jsonschema():
    requirements = RequirementSet()
    requirements.add(Requirement.from_line('jsonschema == 3.0.1'))
    return requirements


@pytest.fixture
def distribution_archive_for_jsonschema(pip, download_dir, requirements_for_jsonschema):
    pip.download_sources(
        requirements_for_jsonschema,
        download_dir,
    )
    for file_name in os.listdir(download_dir):
        if 'jsonschema' in file_name:
            return Archive(path=os.path.join(download_dir, file_name))


@pytest.fixture(params=(
    'six',
    'setuptools == 41.0.1',
))
def requirement(request):
    return Requirement.from_line(request.param)


@pytest.fixture
def source_distribution_archive(pip, requirement, download_dir):
    requirement_set = RequirementSet()
    requirement_set.add(requirement)
    pip.download_sources(
        requirement_set,
        download_dir,
    )
    for file_name in os.listdir(download_dir):
        if file_name.startswith(requirement.name):
            return Archive(path=os.path.join(download_dir, file_name))
    else:
        assert False


@pytest.fixture
def platform_generator(nix):
    return PlatformGenerator(nix)


@pytest.fixture
def current_platform(platform_generator):
    return platform_generator.current_platform()


@pytest.fixture
def test_txt_content():
    path = os.path.join(DATA_DIRECTORY, "test.txt")
    with open(path) as f:
        return f.read()


@pytest.fixture
def test_tar_gz_path():
    return os.path.join(DATA_DIRECTORY, "test.tar.gz")


@pytest.fixture
def test_zip_path():
    return os.path.join(DATA_DIRECTORY, "test.zip")

@pytest.fixture
def test_tar_bz2_path():
    return os.path.join(DATA_DIRECTORY, 'test.tar.bz2')
