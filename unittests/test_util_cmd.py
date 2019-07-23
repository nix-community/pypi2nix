from pypi2nix.utils import cmd


def test_consistent_output():
    exit_code, output = cmd(["seq", "5"])
    assert output == "1\n2\n3\n4\n5\n"
