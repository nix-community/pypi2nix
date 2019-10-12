import pytest

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements_file import RequirementsFile


@pytest.fixture
def requirements_file_from_lines(
    project_dir, tmpdir_factory, requirement_parser, logger: Logger
):
    def factory(lines):
        requirements_file = tmpdir_factory.mktemp("test").join("requirements.txt")
        requirements_file.write("\n".join(lines))
        return RequirementsFile(
            str(requirements_file), project_dir, requirement_parser, logger
        )

    return factory


def test_requirements_file_handles_comments(requirements_file_from_lines):
    requirements_file = requirements_file_from_lines(["# comment"])
    requirements_file.process()


def test_requirements_file_handles_empty_lines(requirements_file_from_lines):
    requirements_file = requirements_file_from_lines([""])
    requirements_file.process()


def test_requirements_file_can_be_created_from_requirements_lines(
    project_dir: str, requirement_parser: RequirementParser, logger: Logger
):
    RequirementsFile.from_lines(
        ["pytest"],
        requirement_parser=requirement_parser,
        project_dir=project_dir,
        logger=logger,
    )


def test_regular_requirements_stay_in_processed_file(
    project_dir: str, requirement_parser: RequirementParser, logger: Logger
):
    requirement_file = RequirementsFile.from_lines(
        ["pytest"],
        requirement_parser=requirement_parser,
        project_dir=project_dir,
        logger=logger,
    )
    processed_file = requirement_file.processed_requirements_file_path()
    with open(processed_file) as f:
        assert "pytest" in f.read()
