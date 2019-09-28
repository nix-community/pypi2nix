import os.path
import venv

import pytest

from pypi2nix.pip.implementation import NixPip
from pypi2nix.pip.virtualenv import VirtualenvPip
from pypi2nix.requirement_parser import RequirementParser


@pytest.fixture(params=("nix", "venv"))
def pip(
    request,
    nix,
    project_dir,
    current_platform,
    logger,
    requirement_parser: RequirementParser,
):
    if request.param == "nix":
        return NixPip(
            nix=nix,
            project_directory=project_dir,
            extra_build_inputs=[],
            extra_env="",
            wheels_cache=[],
            target_platform=current_platform,
            logger=logger,
            requirement_parser=requirement_parser,
        )
    else:
        pip = VirtualenvPip(
            logger=logger,
            target_platform=current_platform,
            target_directory=os.path.join(project_dir, "venv-pip"),
            env_builder=venv.EnvBuilder(with_pip=True),
            requirement_parser=requirement_parser,
        )
        pip.prepare_virtualenv()
        return pip
