import os
import os.path
from io import StringIO

import pytest

from pypi2nix.archive import Archive
from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix
from pypi2nix.pip import Pip
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.wheel import Wheel

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "unittests", "data")


@pytest.fixture
def nix(logger):
    return Nix(logger)


@pytest.fixture
def project_dir(tmpdir):
    return str(tmpdir)


@pytest.fixture
def download_dir(project_dir):
    path = os.path.join(project_dir, "download")
    os.makedirs(path)
    return path


@pytest.fixture
def wheels_dir(project_dir):
    path = os.path.join(project_dir, "wheels")
    os.makedirs(path)
    return path


@pytest.fixture
def pip(nix, project_dir, current_platform):
    return Pip(
        nix=nix,
        project_directory=project_dir,
        extra_build_inputs=[],
        extra_env="",
        verbose=3,
        wheels_cache=[],
        target_platform=current_platform,
    )


@pytest.fixture
def wheel_builder(pip, project_dir, logger, requirement_parser):
    return WheelBuilder(pip, project_dir, logger, requirement_parser)


@pytest.fixture
def extracted_six_package(six_requirements, wheel_builder, default_environment):
    wheels = wheel_builder.build(six_requirements)
    for wheel_directory in wheels:
        wheel = Wheel.from_wheel_directory_path(wheel_directory, default_environment)
        if wheel.name == "six":
            return wheel_directory
    raise Exception('Error when trying to build wheel for "six == 1.12.0"')


@pytest.fixture
def six_requirements(project_dir, current_platform, requirement_parser):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six == 1.12.0"))
    return requirements


@pytest.fixture
def default_environment(pip):
    return pip.default_environment()


@pytest.fixture
def six_source_distribution_archive(pip, download_dir, six_requirements):
    pip.download_sources(six_requirements, download_dir)
    for file_name in os.listdir(download_dir):
        if "six" in file_name:
            return Archive(path=os.path.join(download_dir, file_name))
    raise Exception("Could not create source archive for `six`")


@pytest.fixture
def requirements_for_jsonschema(current_platform, requirement_parser):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("jsonschema == 3.0.1"))
    return requirements


@pytest.fixture
def distribution_archive_for_jsonschema(pip, download_dir, requirements_for_jsonschema):
    pip.download_sources(requirements_for_jsonschema, download_dir)
    for file_name in os.listdir(download_dir):
        if "jsonschema" in file_name:
            return Archive(path=os.path.join(download_dir, file_name))
    raise Exception("Could not download source distribution for `jsonschema`")


@pytest.fixture(params=("six == 1.12.0", "setuptools == 41.0.1"))
def requirement(request, requirement_parser):
    return requirement_parser.parse(request.param)


@pytest.fixture
def source_distribution_archive(pip, requirement, download_dir, current_platform):
    requirement_set = RequirementSet(current_platform)
    requirement_set.add(requirement)
    pip.download_sources(requirement_set, download_dir)
    for file_name in os.listdir(download_dir):
        if file_name.startswith(requirement.name()):
            return Archive(path=os.path.join(download_dir, file_name))
    else:
        raise Exception(
            "Could not download source distribution for `{}`".format(requirement.name())
        )


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
    return os.path.join(DATA_DIRECTORY, "test.tar.bz2")


@pytest.fixture
def data_directory():
    return DATA_DIRECTORY


@pytest.fixture
def logger():
    with StringIO() as f:
        yield StreamLogger(output=f)


@pytest.fixture
def requirement_parser(logger):
    return RequirementParser(logger=logger)
