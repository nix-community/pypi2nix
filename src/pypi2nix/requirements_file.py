import hashlib
import os
import os.path
import tempfile
from typing import List
from typing import Type
from typing import Union

from pypi2nix.requirement_parser import ParsingFailed
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.requirements import PathRequirement

LineHandler = Union[
    "_RequirementIncludeLineHandler", "_EditableLineHandler", "_RequirementLineHandler"
]


class RequirementsFile:
    def __init__(
        self, path: str, project_dir: str, requirement_parser: RequirementParser
    ):
        self.project_dir: str = project_dir
        self.original_path: str = path
        self.requirement_parser = requirement_parser

    @classmethod
    def from_lines(
        constructor: "Type[RequirementsFile]",
        lines: List[str],
        project_dir: str,
        requirement_parser: RequirementParser,
    ) -> "RequirementsFile":
        assert not isinstance(lines, str)
        temporary_file_descriptor, temporary_file_path = tempfile.mkstemp(
            dir=project_dir, text=True
        )
        try:
            with open(temporary_file_descriptor, "w") as f:
                for line in lines:
                    f.write(line)
                    f.write("\n")
            requirements_file = constructor(
                project_dir=project_dir,
                path=temporary_file_path,
                requirement_parser=requirement_parser,
            )
            requirements_file.process()
        finally:
            os.remove(temporary_file_path)
        return requirements_file

    def read(self) -> str:
        if os.path.exists(self.processed_requirements_file_path()):
            path = self.processed_requirements_file_path()
        else:
            path = self.original_path
        with open(path) as f:
            return f.read()

    def process(self) -> None:
        new_requirements_file = self.processed_requirements_file_path()

        with open(self.original_path) as original_file, open(
            new_requirements_file, "w+"
        ) as new_file:
            for requirements_line in original_file.readlines():
                requirements_line = requirements_line.strip()
                if requirements_line:
                    print(self._process_line(requirements_line), file=new_file)

    def _process_line(self, requirements_line: str) -> str:
        line_handler: LineHandler
        if self.is_include_line(requirements_line):
            line_handler = _RequirementIncludeLineHandler(
                line=requirements_line,
                original_path=self.original_path,
                project_directory=self.project_dir,
                requirement_parser=self.requirement_parser,
            )
        elif self.is_editable_line(requirements_line):
            line_handler = _EditableLineHandler(
                line=requirements_line,
                original_path=self.original_path,
                requirement_parser=self.requirement_parser,
            )
        else:
            line_handler = _RequirementLineHandler(
                line=requirements_line,
                requirement_parser=self.requirement_parser,
                original_path=self.original_path,
            )
        return line_handler.process()

    def processed_requirements_file_path(self) -> str:
        return "%s/%s.txt" % (
            self.project_dir,
            hashlib.md5(self.original_path.encode()).hexdigest(),
        )

    def is_include_line(self, line: str) -> bool:
        return line.startswith("-r ") or line.startswith("-c ")

    def is_vcs_line(self, line: str) -> bool:
        return line.startswith("-e git+") or line.startswith("-e hg+")

    def is_editable_line(self, line: str) -> bool:
        return line.startswith("-e ") and not self.is_vcs_line(line)


class _RequirementIncludeLineHandler:
    def __init__(
        self,
        line: str,
        original_path: str,
        project_directory: str,
        requirement_parser: RequirementParser,
    ) -> None:
        self._line = line
        self._original_path = original_path
        self._project_directory = project_directory
        self._requirement_parser = requirement_parser

    def process(self) -> str:
        # this includes '-r ' and '-c ' lines
        original_file_path = self._line[2:].strip()
        if os.path.isabs(original_file_path):
            included_file_path = original_file_path
        else:
            included_file_path = os.path.abspath(
                os.path.join(os.path.dirname(self._original_path), original_file_path)
            )
        new_requirements_file = RequirementsFile(
            included_file_path,
            self._project_directory,
            requirement_parser=self._requirement_parser,
        )
        new_requirements_file.process()
        return (
            self._line[0:3] + new_requirements_file.processed_requirements_file_path()
        )


class _EditableLineHandler:
    def __init__(
        self, line: str, original_path: str, requirement_parser: RequirementParser
    ) -> None:
        self._line = line
        self._original_path = original_path
        self._requirement_parser = requirement_parser

    def process(self) -> str:
        self._strip_editable()
        line_handler = _RequirementLineHandler(
            line=self._line,
            requirement_parser=self._requirement_parser,
            original_path=self._original_path,
        )
        return "-e " + line_handler.process()

    def _strip_editable(self) -> None:
        self._line = self._line[2:].strip()


class _RequirementLineHandler:
    def __init__(
        self, line: str, requirement_parser: RequirementParser, original_path: str
    ) -> None:
        self._line = line
        self._requirement_parser = requirement_parser
        self._original_path = original_path

    def process(self) -> str:
        try:
            requirement = self._requirement_parser.parse(self._line)
        except ParsingFailed:
            return self._line
        else:
            if isinstance(requirement, PathRequirement):
                requirement = requirement.change_path(self._update_path)
            return requirement.to_line()

    def _update_path(self, requirement_path: str) -> str:
        if os.path.isabs(requirement_path):
            return requirement_path
        else:
            absolute_path = os.path.abspath(
                os.path.join(os.path.dirname(self._original_path), requirement_path)
            )
            return absolute_path
