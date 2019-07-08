from pypi2nix.requirement_set import RequirementSet
from pypi2nix.requirements import Requirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources


def test_length_of_empty_requirement_set_is_0():
    assert len(RequirementSet()) == 0


def test_length_is_one_after_adding_one_requirement():
    requirement_set = RequirementSet()
    requirement_set.add(Requirement("pypi2nix"))
    assert len(requirement_set) == 1


def test_length_is_one_after_adding_same_requirement_twice():
    requirement_set = RequirementSet()
    requirement_set.add(Requirement("pypi2nix"))
    requirement_set.add(Requirement("pypi2nix"))
    assert len(requirement_set) == 1


def test_to_file_outputs_a_requirements_file_object(project_dir, current_platform):
    assert isinstance(
        RequirementSet().to_file(project_dir, current_platform), RequirementsFile
    )


def test_sources_contains_a_source_per_git_requirement():
    requirement_set = RequirementSet()
    requirement_set.add(Requirement.from_line("no-git-source"))
    requirement_set.add(Requirement.from_line("git+https://url.test/path#egg=test-egg"))
    assert len(requirement_set.sources) == 1


def test_versions_add_if_same_requirement_is_added_twice():
    requirement_set = RequirementSet()
    requirement_set.add(Requirement.from_line("pypi2nix <= 2.0"))
    requirement_set.add(Requirement.from_line("pypi2nix >= 1.9"))
    requirement = requirement_set.requirements["pypi2nix"]
    assert len(requirement.version) == 2


def test_from_file_handles_empty_lines(project_dir):
    requirements_file = RequirementsFile.from_lines(["pypi2nix", ""], project_dir)
    requirements_set = RequirementSet.from_file(requirements_file)
    assert len(requirements_set) == 1


def test_from_file_handles_comment_lines(project_dir):
    requirements_file = RequirementsFile.from_lines(
        ["pypi2nix", "# comment"], project_dir
    )
    requirements_set = RequirementSet.from_file(requirements_file)
    assert len(requirements_set) == 1


def test_sources_has_sources_type():
    requirement_set = RequirementSet()
    assert isinstance(requirement_set.sources, Sources)


def test_adding_two_empty_sets_results_in_an_empty_set():
    requirements = RequirementSet() + RequirementSet()
    assert len(requirements) == 0


def test_can_find_requirement_in_requirement_set():
    requirements = RequirementSet()
    requirements.add(Requirement.from_line("pypi2nix"))
    assert "pypi2nix" in requirements


def test_cannot_find_name_in_empty_requirement_set():
    assert "test" not in RequirementSet()


def test_elements_from_both_sets_can_be_found_in_sum_of_sets():
    left = RequirementSet()
    left.add(Requirement.from_line("test1"))
    right = RequirementSet()
    right.add(Requirement.from_line("test2"))
    sum = left + right
    assert "test1" in sum
    assert "test2" in sum
