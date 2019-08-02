import hashlib
import os
import os.path
import tempfile
from typing import List
from typing import Type

import click


class RequirementsFile:
    def __init__(self, path: str, project_dir: str):
        self.project_dir: str = project_dir
        self.original_path: str = path

    @classmethod
    def from_lines(
        constructor: "Type[RequirementsFile]", lines: List[str], project_dir: str
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
                project_dir=project_dir, path=temporary_file_path
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

        with open(self.original_path) as f1:
            with open(new_requirements_file, "w+") as f2:
                for requirements_line in f1.readlines():
                    f2.write(self.process_line(requirements_line))
                    f2.write("\n")

    def process_line(self, requirements_line: str) -> str:
        requirements_line = requirements_line.strip()
        if self.is_editable_line(requirements_line):
            requirements_line = self.handle_editable_line(requirements_line)
        elif self.is_include_line(requirements_line):
            requirements_line = self.handle_include_line(requirements_line)
        return requirements_line

    def processed_requirements_file_path(self) -> str:
        return "%s/%s.txt" % (
            self.project_dir,
            hashlib.md5(self.original_path.encode()).hexdigest(),
        )

    def is_include_line(self, line: str) -> bool:
        return line.startswith("-r ") or line.startswith("-c ")

    def handle_include_line(self, line: str) -> str:
        # this includes '-r ' and '-c ' lines
        original_file_path = line[2:].strip()
        if os.path.isabs(original_file_path):
            included_file_path = original_file_path
        else:
            included_file_path = os.path.abspath(
                os.path.join(os.path.dirname(self.original_path), original_file_path)
            )
        new_requirements_file = RequirementsFile(included_file_path, self.project_dir)
        new_requirements_file.process()
        return line[0:3] + new_requirements_file.processed_requirements_file_path()

    def is_vcs_line(self, line: str) -> bool:
        return line.startswith("-e git+") or line.startswith("-e hg+")

    def is_editable_line(self, line: str) -> bool:
        return line.startswith("-e ") and not self.is_vcs_line(line)

    def handle_editable_line(self, line: str) -> str:
        line = line[3:]
        try:
            tmp_path, _ = line.split("#")
            tmp_path = tmp_path.strip()
            _tmp = tmp_path.split("[")
            if len(_tmp) > 1:
                tmp_path = _tmp[0]
                tmp_other = "[" + _tmp[1]
            else:
                tmp_other = ""
        except Exception:
            raise click.ClickException(
                "Requirement starting with `.` "
                "should end with #egg=<name>. Line `%s` does "
                "not end with egg=<name>" % line
            )

        tmp_path = os.path.abspath(
            os.path.join(
                os.path.dirname(self.original_path),
                os.path.abspath(os.path.join(os.getcwd(), tmp_path)),
            )
        )
        return "-e %s%s" % (tmp_path, tmp_other)
