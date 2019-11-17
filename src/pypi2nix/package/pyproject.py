import toml

from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import ParsingFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirement_set import RequirementSet
from pypi2nix.target_platform import TargetPlatform

from .interfaces import HasBuildDependencies


class PyprojectToml(HasBuildDependencies):
    def __init__(
        self,
        name: str,
        file_content: str,
        logger: Logger,
        requirement_parser: RequirementParser,
    ) -> None:
        self.pyproject_toml = toml.loads(file_content)
        self.logger = logger
        self.requirement_parser = requirement_parser
        self.name = name

    def build_dependencies(self, target_platform: TargetPlatform) -> RequirementSet:
        requirement_set = RequirementSet(target_platform)
        if self.pyproject_toml is not None:
            for build_input in self.pyproject_toml.get("build-system", {}).get(
                "requires", []
            ):
                try:
                    requirement = self.requirement_parser.parse(build_input)
                except ParsingFailed as e:
                    self.logger.warning(
                        "Failed to parse build dependency of `{name}`".format(
                            name=self.name
                        )
                    )
                    self.logger.warning(
                        "Possible reason: `{reason}`".format(reason=e.reason)
                    )
                else:
                    if requirement.applies_to_target(target_platform):
                        requirement_set.add(requirement)
        return requirement_set
