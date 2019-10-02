import pytest

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import VersionRequirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources
from pypi2nix.target_platform import TargetPlatform


@pytest.fixture
def requirement_set(current_platform):
    return RequirementSet(current_platform)


def test_length_of_empty_requirement_set_is_0(current_platform):
    assert len(RequirementSet(current_platform)) == 0


def test_length_is_one_after_adding_one_requirement(
    current_platform, requirement_parser
):
    requirement_set = RequirementSet(current_platform)
    requirement_set.add(requirement_parser.parse("pypi2nix"))
    assert len(requirement_set) == 1


def test_length_is_one_after_adding_same_requirement_twice(
    current_platform, requirement_parser
):
    requirement_set = RequirementSet(current_platform)
    requirement_set.add(requirement_parser.parse("pypi2nix"))
    requirement_set.add(requirement_parser.parse("pypi2nix"))
    assert len(requirement_set) == 1


def test_to_file_outputs_a_requirements_file_object(
    project_dir, current_platform, requirement_parser, logger: Logger
):
    assert isinstance(
        RequirementSet(current_platform).to_file(
            project_dir, current_platform, requirement_parser, logger
        ),
        RequirementsFile,
    )


def test_sources_contains_a_source_per_git_requirement(
    current_platform, requirement_parser
):
    requirement_set = RequirementSet(current_platform)
    requirement_set.add(requirement_parser.parse("no-git-source"))
    requirement_set.add(
        requirement_parser.parse("git+https://url.test/path#egg=test-egg")
    )
    assert len(requirement_set.sources()) == 1


def test_versions_add_if_same_requirement_is_added_twice(
    current_platform, requirement_parser
):
    requirement_set = RequirementSet(current_platform)
    requirement_set.add(requirement_parser.parse("pypi2nix <= 2.0"))
    requirement_set.add(requirement_parser.parse("pypi2nix >= 1.9"))
    requirement = requirement_set.requirements["pypi2nix"]
    assert isinstance(requirement, VersionRequirement)
    assert len(requirement.version()) == 2


def test_from_file_handles_empty_lines(
    project_dir, current_platform, requirement_parser, logger: Logger
):
    requirements_file = RequirementsFile.from_lines(
        ["pypi2nix", ""], project_dir, requirement_parser, logger
    )
    requirements_set = RequirementSet.from_file(
        requirements_file, current_platform, requirement_parser, logger
    )
    assert len(requirements_set) == 1


def test_from_file_handles_comment_lines(
    project_dir, current_platform, requirement_parser, logger: Logger
):
    requirements_file = RequirementsFile.from_lines(
        ["pypi2nix", "# comment"], project_dir, requirement_parser, logger
    )
    requirements_set = RequirementSet.from_file(
        requirements_file, current_platform, requirement_parser, logger
    )
    assert len(requirements_set) == 1


def test_sources_has_sources_type(current_platform):
    requirement_set = RequirementSet(current_platform)
    assert isinstance(requirement_set.sources(), Sources)


def test_adding_two_empty_sets_results_in_an_empty_set(current_platform):
    requirements = RequirementSet(current_platform) + RequirementSet(current_platform)
    assert len(requirements) == 0


def test_can_find_requirement_in_requirement_set(current_platform, requirement_parser):
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("pypi2nix"))
    assert "pypi2nix" in requirements


def test_cannot_find_name_in_empty_requirement_set(current_platform):
    assert "test" not in RequirementSet(current_platform)


def test_elements_from_both_sets_can_be_found_in_sum_of_sets(
    current_platform, requirement_parser
):
    left = RequirementSet(current_platform)
    left.add(requirement_parser.parse("test1"))
    right = RequirementSet(current_platform)
    right.add(requirement_parser.parse("test2"))
    sum = left + right
    assert "test1" in sum
    assert "test2" in sum


def test_requirement_set_respects_constraints_when_reading_from_requirement_file(
    tmpdir, project_dir, current_platform, requirement_parser, logger: Logger
):
    requirements_txt = tmpdir.join("requirements.txt")
    constraints_txt = tmpdir.join("constraints.txt")
    with open(requirements_txt, "w") as f:
        print("test-requirement", file=f)
        print("-c " + str(constraints_txt), file=f)
    with open(constraints_txt, "w") as f:
        print("test-requirement <= 1.0", file=f)

    original_requirements_file = RequirementsFile(
        str(requirements_txt), project_dir, requirement_parser, logger
    )
    original_requirements_file.process()

    requirement_set = RequirementSet.from_file(
        original_requirements_file, current_platform, requirement_parser, logger
    )

    new_requirements_file = requirement_set.to_file(
        project_dir, current_platform, requirement_parser, logger
    )

    assert "test-requirement <= 1.0" in new_requirements_file.read()


def test_constraints_without_requirement_will_not_show_up_in_generated_requirement_file(
    tmpdir, project_dir, current_platform, requirement_parser, logger: Logger
):
    requirements_txt = tmpdir.join("requirements.txt")
    constraints_txt = tmpdir.join("constraints.txt")

    with open(requirements_txt, "w") as f:
        print("test-requirement", file=f)
        print("-c " + str(constraints_txt), file=f)
    with open(constraints_txt, "w") as f:
        print("test-constraint == 1.0", file=f)

    original_requirements_file = RequirementsFile(
        str(requirements_txt), project_dir, requirement_parser, logger
    )
    original_requirements_file.process()

    requirement_set = RequirementSet.from_file(
        original_requirements_file, current_platform, requirement_parser, logger
    )

    new_requirements_file = requirement_set.to_file(
        project_dir, current_platform, requirement_parser, logger
    )

    assert "test-constraint" not in new_requirements_file.read()


def test_include_lines_are_respected_when_generating_from_file(
    tmpdir, project_dir, current_platform, requirement_parser, logger: Logger
):
    requirements_txt = tmpdir.join("requirements.txt")
    included_requirements_txt = tmpdir.join("included_requirements.txt")

    with open(requirements_txt, "w") as f:
        print("-r " + str(included_requirements_txt), file=f)
    with open(included_requirements_txt, "w") as f:
        print("test-requirement", file=f)
    requirements_file = RequirementsFile(
        str(requirements_txt), project_dir, requirement_parser, logger
    )
    requirements_file.process()
    requirement_set = RequirementSet.from_file(
        requirements_file, current_platform, requirement_parser, logger
    )

    assert "test-requirement" in requirement_set


def test_that_we_can_query_for_added_requirements(requirement_set, requirement_parser):
    requirement = requirement_parser.parse("pytest")
    requirement_set.add(requirement)
    assert requirement_set[requirement.name()] == requirement


def test_that_querying_for_non_existing_requirement_raises_key_error(requirement_set):
    with pytest.raises(KeyError):
        requirement_set["non-existing"]


def test_that_queries_into_set_are_canonicalized(requirement_set, requirement_parser):
    requirement = requirement_parser.parse("pytest")
    requirement_set.add(requirement)
    assert requirement_set["PyTest"] == requirement


def test_that_get_method_returns_none_if_key_not_found(requirement_set):
    assert requirement_set.get("not-found") is None


def test_that_get_method_returns_specified_default_value_when_not_found(
    requirement_set
):
    assert requirement_set.get("not-found", 0) == 0


def test_that_filter_works_by_name(requirement_parser, requirement_set):
    requirement = requirement_parser.parse("test")
    requirement_set.add(requirement)

    assert len(requirement_set) == 1

    filtered_requirement_set = requirement_set.filter(lambda req: req.name() != "test")

    assert len(filtered_requirement_set) == 0


def test_that_extras_are_preserved_when_converting_to_and_from_a_file(
    requirement_parser: RequirementParser,
    requirement_set: RequirementSet,
    current_platform: TargetPlatform,
    project_dir: str,
    logger: Logger,
):
    requirement_set.add(requirement_parser.parse("req[extra1]"))
    requirements_file = requirement_set.to_file(
        project_dir, current_platform, requirement_parser, logger
    )
    new_requirements_set = RequirementSet.from_file(
        requirements_file, current_platform, requirement_parser, logger
    )
    requirement = new_requirements_set["req"]
    assert requirement.extras() == {"extra1"}
