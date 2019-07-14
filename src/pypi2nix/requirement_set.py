import os.path
import tempfile

from pypi2nix.requirements import ParsingFailed
from pypi2nix.requirements import Requirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources


class RequirementSet:
    def __init__(self, target_platform):
        self.requirements = dict()
        self.constraints = dict()
        self.target_platform = target_platform

    def add(self, requirement):
        if requirement.name in self.requirements:
            self.requirements[requirement.name] = self.requirements[
                requirement.name
            ].add(requirement, self.target_platform)
        elif requirement.name in self.constraints:
            self.requirements[requirement.name] = self.constraints[requirement.name]
            del self.constraints[requirement.name]
            self.add(requirement)
        else:
            self.requirements[requirement.name] = requirement

    def __len__(self):
        return len(self.requirements)

    def to_file(self, project_dir, target_platform):
        with tempfile.TemporaryDirectory() as directory:
            requirements_txt = os.path.join(directory, "requirements.txt")
            constraints_txt = os.path.join(directory, "constraints.txt")
            with open(requirements_txt, "w") as f:
                print(self.requirements_file_content(target_platform), file=f)
                print("-c " + constraints_txt, file=f)
            with open(constraints_txt, "w") as f:
                print(self.constraints_file_content(target_platform), file=f)
            requirements_file = RequirementsFile(requirements_txt, project_dir)
            requirements_file.process()
        return requirements_file

    def add_constraint(self, requirement):
        if requirement.name in self.requirements:
            self.add(requirement)
        elif requirement.name in self.constraints:
            self.constraints[requirement.name] = self.constraints[requirement.name].add(
                requirement, self.target_platform
            )
        else:
            self.constraints[requirement.name] = requirement

    def to_constraints_only(self):
        new_requirement_set = RequirementSet(self.target_platform)
        for requirement in list(self.requirements.values()) + list(
            self.constraints.values()
        ):
            new_requirement_set.add_constraint(requirement)
        return new_requirement_set

    @classmethod
    def from_file(constructor, requirements_file, target_platform):
        file_lines = requirements_file.read().splitlines()
        requirements_set = constructor(target_platform)
        for line in file_lines:
            try:
                requirement = Requirement.from_line(line)
            except ParsingFailed:
                detected_requirements = constructor.handle_non_requirement_line(
                    line, target_platform
                )
                requirements_set += detected_requirements
            else:
                requirements_set.add(requirement)
        return requirements_set

    @classmethod
    def handle_non_requirement_line(constructor, line, target_platform):
        line = line.strip()
        if line.startswith("-c "):
            include_path = line[2:].strip()
            with tempfile.TemporaryDirectory() as project_directory:
                requirements_file = RequirementsFile(include_path, project_directory)
                requirements_file.process()
                return constructor.from_file(
                    requirements_file, target_platform
                ).to_constraints_only()
        elif line.startswith("-r "):
            include_path = line[2:].strip()
            with tempfile.TemporaryDirectory() as project_directory:
                requirements_file = RequirementsFile(include_path, project_directory)
                requirements_file.process()
                return constructor.from_file(requirements_file, target_platform)
        else:
            return constructor(target_platform)

    def sources(self):
        sources = Sources()
        for requirement in self.requirements.values():
            if requirement.source is None:
                continue
            else:
                sources.add(requirement.name, requirement.source)
        return sources

    def requirements_file_content(self, target_platform):
        return self.requirements_to_file_content(
            self.requirements.values(), target_platform
        )

    def constraints_file_content(self, target_platform):
        return self.requirements_to_file_content(
            self.constraints.values(), target_platform
        )

    @classmethod
    def requirements_to_file_content(_, requirements, target_platform):
        return "\n".join(
            [
                requirement.to_line()
                for requirement in requirements
                if requirement.applies_to_target(target_platform)
            ]
        )

    def __add__(self, other):
        requirement_set = RequirementSet(self.target_platform)

        requirements = list(self.requirements.values()) + list(
            other.requirements.values()
        )
        for requirement in requirements:
            requirement_set.add(requirement)

        constraints = list(self.constraints.values()) + list(other.constraints.values())
        for constraint in constraints:
            requirement_set.add_constraint(constraint)

        return requirement_set

    def __contains__(self, name):
        return name in self.requirements

    def __iter__(self):
        yield from self.requirements.values()
