import os.path

from pypi2nix.requirement_parser import requirement_parser
from pypi2nix.requirement_set import RequirementSet

from ..switches import nix


@nix
def test_freeze_on_empty_environment_yields_empty_file(pip):
    frozen_requirements = pip.freeze()
    assert not frozen_requirements


@nix
def test_freeze_respects_additional_python_path(pip, project_dir, current_platform):
    prefix = os.path.join(project_dir, "custom-prefix")
    download_dir = os.path.join(project_dir, "download")
    requirements = RequirementSet(current_platform)
    requirements.add(requirement_parser.parse("six"))
    pip.download_sources(requirements, download_dir)
    pip.install(
        requirements, target_directory=prefix, source_directories=[download_dir]
    )
    freeze_without_six = pip.freeze()
    freeze_with_six = pip.freeze(python_path=[prefix])
    assert len(freeze_without_six) < len(freeze_with_six)
