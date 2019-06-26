import click
import pytest

from pypi2nix.nix import EvaluationFailed
from pypi2nix.stage1 import WheelBuilder


def test_wheel_builder_raises_click_exception_when_nix_shell_command_fails(
        tmpdir,
):
    class Nix:
        def shell(self, *args, **kwargs):
            raise EvaluationFailed(output="test output")

        def evaluate_expression(self, *args, **kwargs):
            return ""

    project_dir = str(tmpdir.join('project_dir'))

    wheel_builder = WheelBuilder(
        requirements_files=[],
        project_dir=project_dir,
        download_cache_dir=None,
        wheel_cache_dir=None,
        extra_build_inputs=None,
        python_version=3,
        nix=Nix(),
    )
    with pytest.raises(click.ClickException):
        wheel_builder.build()
