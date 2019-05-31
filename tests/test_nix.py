import os.path

import pytest
from pypi2nix.nix import *

HERE = os.path.dirname(__file__)


nix = pytest.mark.nix


@pytest.fixture
def nix_instance(tmpdir):
    nix_path_addition = tmpdir.mkdir("testpath_exists")
    yield Nix(nix_path=["test_variable={}".format(str(nix_path_addition))])


@pytest.fixture
def dummy_derivation():
    return os.path.join(HERE, "data/shell_environment.nix")


@nix
def test_evaluate_nix_expression_works(nix_instance):
    assert nix_instance.evaluate_expression("1 + 1") == "2"


@nix
def test_evalulate_nix_expression_respects_additions_to_nix_path(nix_instance):
    assert "testpath_exists" in nix_instance.evaluate_expression("<test_variable>")


@nix
def test_evaluate_nix_expression_raises_exception_when_executable_not_found():
    nix = Nix(executable_directory="/does-not-exist")
    with pytest.raises(ExecutableNotFound):
        nix.evaluate_expression("true")


@nix
def test_shell_accepts_file_path_to_run_shell_script(nix_instance, dummy_derivation):
    output = nix_instance.shell("echo $out", derivation_path=dummy_derivation)
    assert "hello" in output


@nix
def test_shell_accepts_nix_arguments(nix_instance, dummy_derivation):
    output = nix_instance.shell(
        "echo $out",
        derivation_path=dummy_derivation,
        nix_arguments={"dummy_argument": "perl"},
    )
    assert "perl" in output


@nix
def test_evaluate_expression_throws_on_erroneous_expression(nix_instance):
    with pytest.raises(EvaluationFailed):
        nix_instance.evaluate_expression('1+')
