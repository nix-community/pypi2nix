import pytest
from pypi2nix.nix import Nix
from pypi2nix.pip import Pip


@pytest.fixture
def nix():
    return Nix(verbose=True)


@pytest.fixture
def project_dir(tmpdir):
    return str(tmpdir)


@pytest.fixture
def pip(nix, project_dir):
    return Pip(
        nix=nix,
        project_directory=project_dir,
        extra_build_inputs=[],
        python_version="python3",
        extra_env="",
        verbose=3,
        wheels_cache=[],
    )
