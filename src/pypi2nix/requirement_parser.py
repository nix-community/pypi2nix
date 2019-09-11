from typing import no_type_check

import parsley

from pypi2nix.requirement_parser_grammar import requirement_parser_grammar
from pypi2nix.requirements import Logger
from pypi2nix.requirements import Requirement


class ParsingFailed(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason

    def __str__(self) -> str:
        return self.reason


class RequirementParser:
    def __init__(self, logger: Logger) -> None:
        self._compiled_grammar = None
        self.logger = logger

    @no_type_check
    def compiled_grammar(self):
        with requirement_parser_grammar(self.logger) as grammar:
            return grammar

    def parse(self, line: str) -> Requirement:
        line = line.strip()
        if "\n" in line:
            raise ParsingFailed(
                "Failed to parse requirement from string `{}`".format(line)
            )
        try:
            return self.compiled_grammar()(line).specification()  # type: ignore
        except parsley.ParseError as e:
            raise ParsingFailed("{message}".format(message=e.formatError()))
