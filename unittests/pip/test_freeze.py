from ..switches import nix


@nix
def test_freeze_on_empty_environment_yields_empty_file(pip):
    frozen_requirements = pip.freeze()
    assert not frozen_requirements
