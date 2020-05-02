from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.requirement_parser import RequirementParser

from .framework import IntegrationTest


class DependencyGraphTestCase(IntegrationTest):
    name_of_testcase = "dependency_graph"
    requirements = ["django == 3.0.5"]

    def check_dependency_graph(
        self, dependency_graph: DependencyGraph, requirement_parser: RequirementParser
    ):
        self.assertTrue(
            dependency_graph.is_runtime_dependency(
                requirement_parser.parse("django"), requirement_parser.parse("pytz"),
            )
        )
