from pypi2nix.dependency_graph import DependencyGraph
from pypi2nix.requirement_parser import RequirementParser

from .framework import IntegrationTest


class DependencyGraphOutputTestCase(IntegrationTest):
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


class DependencyGraphInputTestCase(IntegrationTest):
    """This class checks behavior if the user supplies a dependency graph
    when running pypi2nix.

    Normally requests should not come with django.  In this test case
    we tell pypi2nix that requests is a dependecy of django.  After
    running pypi2nix nix we check if requests was also installed.
    """

    name_of_testcase = "dependency_graph_input"
    requirements = ["django == 3.0.5"]
    dependency_graph = {"django": {"runtimeDependencies": ["requests"]}}
    code_for_testing = ["import requests"]
