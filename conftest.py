import os
import os.path
import venv
from io import StringIO

import pytest

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.logger import StreamLogger
from pypi2nix.nix import Nix
from pypi2nix.package_source import PathSource
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.pypi import Pypi
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.sources import Sources
from pypi2nix.stage1 import WheelBuilder
from pypi2nix.target_platform import PlatformGenerator
from pypi2nix.target_platform import TargetPlatform
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
def wheel_builder(pip, project_dir, logger, requirement_parser, current_platform):
    return WheelBuilder(pip, project_dir, logger, requirement_parser, current_platform)


@pytest.fixture
def extracted_six_package(
    six_requirements, wheel_builder, current_platform, logger, requirement_parser
):
    wheels = wheel_builder.build(six_requirements)
    for wheel_directory in wheels:
        wheel = Wheel.from_wheel_directory_path(
            wheel_directory, current_platform, logger, requirement_parser
        )
        if wheel.name == "six":
            return wheel_directory
    raise Exception('Error when trying to build wheel for "six == 1.12.0"')


@pytest.fixture
def six_requirements(current_platform, requirement_parser):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six == 1.12.0"))
    return requirements


@pytest.fixture
def six_source_distribution_archive(data_directory):
    return Archive(path=os.path.join(data_directory, "six-1.12.0.tar.gz"))


@pytest.fixture
def distribution_archive_for_jsonschema(data_directory):
    return Archive(path=os.path.join(data_directory, "jsonschema-3.0.1.tar.gz"))


@pytest.fixture(params=("six == 1.12.0", "setuptools == 41.0.1"))
def requirement(request, requirement_parser):
    return requirement_parser.parse(request.param)


@pytest.fixture
def setupcfg_package_wheel_path(data_directory: str) -> str:
    return os.path.join(data_directory, "setupcfg_package-1.0-py3-none-any.whl")


@pytest.fixture
def setupcfg_package_wheel(
    setupcfg_package_wheel_path: str,
    logger: Logger,
    requirement_parser: RequirementParser,
    current_platform: TargetPlatform,
) -> Wheel:
    archive = Archive(path=setupcfg_package_wheel_path)
    with archive.extracted_files() as directory:
        return Wheel.from_wheel_directory_path(
            os.path.join(directory, "setupcfg_package-1.0.dist-info"),
            current_platform,
            logger,
            requirement_parser,
        )


@pytest.fixture
def pip(
    logger: Logger,
    current_platform: TargetPlatform,
    project_dir: str,
    wheel_distribution_archive_path: str,
    data_directory: str,
    requirement_parser: RequirementParser,
) -> VirtualenvPip:
    pip = VirtualenvPip(
        logger=logger,
        target_platform=current_platform,
        target_directory=os.path.join(project_dir, "pip-without-index-venv"),
        env_builder=venv.EnvBuilder(with_pip=True),
        no_index=True,
        wheel_distribution_path=wheel_distribution_archive_path,
        find_links=[data_directory],
        requirement_parser=requirement_parser,
    )
    pip.prepare_virtualenv()
    return pip


@pytest.fixture(params=("six-1.12.0.tar.gz", "jsonschema-3.0.1.tar.gz"))
def source_distribution_archive(request, data_directory):
    return Archive(path=os.path.join(data_directory, request.param))


@pytest.fixture
def platform_generator(nix: Nix) -> PlatformGenerator:
    return PlatformGenerator(nix)


@pytest.fixture
def current_platform(platform_generator: PlatformGenerator) -> TargetPlatform:
    platform = platform_generator.current_platform()
    if platform is None:
        raise Exception("Could not recognize current platform")
    else:
        return platform


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


@pytest.fixture
def wheel_distribution_archive_path(data_directory):
    return os.path.join(data_directory, "wheel-0.33.6-py2.py3-none-any.whl")


@pytest.fixture
def sources_for_test_packages(data_directory):
    sources = Sources()
    package_names = ["setupcfg-package", "package1", "package2", "package3", "package4"]
    for package_name in package_names:
        sources.add(
            package_name,
            PathSource(os.path.join(data_directory, f"{package_name}-1.0.tar.gz")),
        )
    return sources


@pytest.fixture
def pypi(logger: Logger) -> Pypi:
    return Pypi(logger=logger)


@pytest.fixture
def flit_wheel(data_directory, current_platform, logger, requirement_parser):
    path = os.path.join(data_directory, "flit-1.3-py3-none-any.whl")
    with Archive(path=path).extracted_files() as wheel_directory:
        return Wheel.from_wheel_directory_path(
            os.path.join(wheel_directory, "flit-1.3.dist-info"),
            current_platform,
            logger,
            requirement_parser,
        )
