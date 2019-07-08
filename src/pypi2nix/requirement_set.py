from pypi2nix.requirements import ParsingFailed
from pypi2nix.requirements import Requirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources


class RequirementSet:
    def __init__(self):
        self.requirements = dict()

    def add(self, requirement):
        if requirement.name in self.requirements:
            self.requirements[requirement.name].version += requirement.version
        else:
            self.requirements[requirement.name] = requirement

    def __len__(self):
        return len(self.requirements)

    def to_file(self, project_dir, target_platform):
        return RequirementsFile.from_lines(
            self.requirements_file_content(target_platform), project_dir
        )

    @classmethod
    def from_file(constructor, requirements_file):
        file_lines = requirements_file.read().splitlines()
        requirements_set = constructor()
        for line in file_lines:
            try:
                requirement = Requirement.from_line(line)
            except ParsingFailed:
                continue
            requirements_set.add(requirement)
        return requirements_set

    @property
    def sources(self):
        sources = Sources()
        for requirement in self.requirements.values():
            if requirement.source is None:
                continue
            else:
                sources.add(requirement.name, requirement.source)
        return sources

    def requirements_file_content(self, target_platform):
        return [
            requirement.to_line()
            for requirement in self.requirements.values()
            if requirement.applies_to_target(target_platform)
        ]

    def __add__(self, other):
        requirements = RequirementSet()
        for requirement in self.requirements.values():
            requirements.add(requirement)
        for requirement in other.requirements.values():
            requirements.add(requirement)
        return requirements

    def __contains__(self, name):
        return name in self.requirements
