import click
from markerlib import interpret
from pypi2nix.package_source import GitSource
from pypi2nix.package_source import HgSource
from pypi2nix.package_source import UrlSource


class ParsingFailed(Exception):
    pass


class Requirement:
    def __init__(self, line):
        if "\n" in line:
            raise ParsingFailed(
                " ".join(
                    [
                        "Requirements file entry {line} seems to contain a newline",
                        "character which is currently not supported",
                    ]
                ).format(line=line)
            )

        self.line = line.strip()
        self.name = None
        self.source = None
        self.is_editable = None
        self.environment_marker = None

        self.parse()

    def applies_to_system(self):
        return interpret(self.environment_marker)

    def parse(self):
        self.detect_environment_marker()
        self.detect_editable()
        self.detect_source()

    def detect_environment_marker(self):
        segments = self.line.split(";")
        if len(segments) > 1:
            self.environment_marker = ";".join(segments[1:]).strip()
            self.line = segments[0]

    def detect_editable(self):
        if self.is_editable is None:
            if self.line.startswith("-e "):
                self.is_editable = True
                self.line = self.line[3:].strip()
            else:
                self.is_editable = False

    def detect_source(self):
        line = self.line
        if (
            line.startswith("http://")
            or line.startswith("https://")
            or line.startswith("git+")
            or line.startswith("hg+")
        ):
            try:
                url, egg = line.split("#")
                self.name = egg.split("egg=")[1]
            except (ValueError, IndexError):
                raise click.ClickException(
                    "Requirement starting with http:// or https:// "
                    "should end with #egg=<name>. Line `-e %s` does "
                    "not end with egg=<name>" % line
                )
            if line.startswith("git+"):
                self.handle_git_source(url)
            elif line.startswith("hg+"):
                self.handle_hg_source(url)
            else:
                self.source = UrlSource(url)
        else:
            self.name = line

    def handle_git_source(self, url):
        if url.startswith("git+"):
            url = url[4:]
        revision = None
        if "@" in url:
            url, revision = url.split("@")
        self.source = GitSource(url, revision)

    def handle_hg_source(self, url):
        if url.startswith("hg+"):
            url = url[3:]
        revision = None
        if "@" in url:
            url, revision = url.split("@")
        self.source = HgSource(url, revision)
