import os.path
import tempfile
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import TypeVar
from typing import Union

from packaging.utils import canonicalize_name

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import ParsingFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements import Requirement
from pypi2nix.requirements_file import RequirementsFile
from pypi2nix.sources import Sources
from pypi2nix.target_platform import TargetPlatform

T = TypeVar("T")


class RequirementSet:
    def __init__(self, target_platform: TargetPlatform) -> None:
        self.requirements: Dict[str, Requirement] = dict()
        self.constraints: Dict[str, Requirement] = dict()
        self.target_platform = target_platform

    def add(self, requirement: Requirement) -> None:
        if requirement.name() in self.requirements:
            self.requirements[requirement.name()] = self.requirements[
                requirement.name()
            ].add(requirement, self.target_platform)
        elif requirement.name() in self.constraints:
            self.requirements[requirement.name()] = self.constraints[requirement.name()]
            del self.constraints[requirement.name()]
            self.add(requirement)
        else:
            self.requirements[requirement.name()] = requirement

    def to_file(
        self,
        project_dir: str,
        target_platform: TargetPlatform,
        requirement_parser: RequirementParser,
        logger: Logger,
    ) -> RequirementsFile:
        with tempfile.TemporaryDirectory() as directory:
            requirements_txt = os.path.join(directory, "requirements.txt")
            constraints_txt = os.path.join(directory, "constraints.txt")
            with open(requirements_txt, "w") as f:
                print(self._requirements_file_content(target_platform), file=f)
                print("-c " + constraints_txt, file=f)
            with open(constraints_txt, "w") as f:
                print(self._constraints_file_content(target_platform), file=f)
            requirements_file = RequirementsFile(
                requirements_txt, project_dir, requirement_parser, logger=logger
            )
            requirements_file.process()
        return requirements_file

    def add_constraint(self, requirement: Requirement) -> None:
        if requirement.name() in self.requirements:
            self.add(requirement)
        elif requirement.name() in self.constraints:
            self.constraints[requirement.name()] = self.constraints[
                requirement.name()
            ].add(requirement, self.target_platform)
        else:
            self.constraints[requirement.name()] = requirement

    def filter(
        self, filter_function: Callable[[Requirement], bool]
    ) -> "RequirementSet":
        filtered_requirement_set = RequirementSet(self.target_platform)
        filtered_requirement_set.constraints = self.constraints
        for requirement in self:
            if filter_function(requirement):
                filtered_requirement_set.add(requirement)
        return filtered_requirement_set

    def to_constraints_only(self) -> "RequirementSet":
        new_requirement_set = RequirementSet(self.target_platform)
        for requirement in list(self.requirements.values()) + list(
            self.constraints.values()
        ):
            new_requirement_set.add_constraint(requirement)
        return new_requirement_set

    @classmethod
    def from_file(
        constructor,
        requirements_file: RequirementsFile,
        target_platform: TargetPlatform,
        requirement_parser: RequirementParser,
        logger: Logger,
    ) -> "RequirementSet":
        file_lines = requirements_file.read().splitlines()
        requirements_set = constructor(target_platform)
        for line in file_lines:
            try:
                requirement = requirement_parser.parse(line)
            except ParsingFailed:
                detected_requirements = constructor._handle_non_requirement_line(
                    line, target_platform, requirement_parser, logger
                )
                requirements_set += detected_requirements
            else:
                requirements_set.add(requirement)
        return requirements_set

    def sources(self) -> Sources:
        sources = Sources()
        for requirement in self.requirements.values():
            source = requirement.source()
            if source is None:
                continue
            else:
                sources.add(requirement.name(), source)
        return sources

    def get(self, key: str, default: Optional[T] = None) -> Union[Requirement, None, T]:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return len(self.requirements)

    def __add__(self, other: "RequirementSet") -> "RequirementSet":
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

    def __contains__(self, name: str) -> bool:
        return name in self.requirements

    def __iter__(self) -> Iterator[Requirement]:
        yield from self.requirements.values()

    def __getitem__(self, key: str) -> Requirement:
        return self.requirements[canonicalize_name(key)]

    def _requirements_file_content(self, target_platform: TargetPlatform) -> str:
        return self._requirements_to_file_content(
            self.requirements.values(), target_platform
        )

    def _constraints_file_content(self, target_platform: TargetPlatform) -> str:
        return self._requirements_to_file_content(
            self.constraints.values(), target_platform
        )

    @classmethod
    def _requirements_to_file_content(
        _, requirements: Iterable[Requirement], target_platform: TargetPlatform
    ) -> str:
        return "\n".join(
            [
                requirement.to_line()
                for requirement in requirements
                if requirement.applies_to_target(target_platform)
            ]
        )

    @classmethod
    def _handle_non_requirement_line(
        constructor,
        line: str,
        target_platform: TargetPlatform,
        requirement_parser: RequirementParser,
        logger: Logger,
    ) -> "RequirementSet":
        line = line.strip()
        if line.startswith("-c "):
            include_path = line[2:].strip()
            with tempfile.TemporaryDirectory() as project_directory:
                requirements_file = RequirementsFile(
                    include_path, project_directory, requirement_parser, logger
                )
                requirements_file.process()
                return constructor.from_file(
                    requirements_file, target_platform, requirement_parser, logger
                ).to_constraints_only()
        elif line.startswith("-r "):
            include_path = line[2:].strip()
            with tempfile.TemporaryDirectory() as project_directory:
                requirements_file = RequirementsFile(
                    include_path, project_directory, requirement_parser, logger
                )
                requirements_file.process()
                return constructor.from_file(
                    requirements_file, target_platform, requirement_parser, logger
                )
        else:
            return constructor(target_platform)
