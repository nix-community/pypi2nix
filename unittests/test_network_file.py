import os.path
import tempfile

import pytest

from pypi2nix.logger import Logger
from pypi2nix.network_file import DiskTextFile
from pypi2nix.network_file import GitTextFile
from pypi2nix.network_file import NetworkFile
from pypi2nix.network_file import UrlTextFile
from pypi2nix.nix import Nix

from .switches import nix


@nix
def test_calculate_sha256_for_text_file(logger: Logger):
    test_file = UrlTextFile(
        url="https://raw.githubusercontent.com/nix-community/pypi2nix/6fe6265b62b53377b4677a39c6ee48550c1f2186/.gitignore",
        logger=logger,
        name="testname",
    )
    assert "*.pyc" in test_file.fetch()
    assert "0b2s1lyfr12v83rrb69j1cfcsksisgwyzfl5mix6qz5ldxfww8p0" == test_file.sha256


@nix
def test_can_evaluate_expression_of_fetched_file(logger: Logger, nix: Nix) -> None:
    test_file = UrlTextFile(
        url="https://raw.githubusercontent.com/nix-community/pypi2nix/6fe6265b62b53377b4677a39c6ee48550c1f2186/.gitignore",
        logger=logger,
        name="testname",
    )
    nix.build_expression(
        expression=f"let pkgs = import <nixpkgs> {{}}; in {test_file.nix_expression() }"
    )


@nix
def test_can_calculate_hash_for_git_files(logger: Logger):
    repository_url = "https://github.com/nix-community/pypi2nix.git"
    path = ".gitignore"
    revision_name = "e56cbbce0812359e80ced3d860e1f232323b2976"
    network_file = GitTextFile(
        repository_url=repository_url,
        revision_name=revision_name,
        path=path,
        logger=logger,
    )

    assert network_file.sha256 == "1vhdippb0daszp3a0m3zb9qcb25m6yib4rpggaiimg7yxwwwzyh4"
    assert "*.pyc" in network_file.fetch()


@nix
def test_can_evaluate_nix_expression(network_file: NetworkFile, nix: Nix):
    expression = f"let pkgs = import <nixpkgs> {{}}; in {network_file.nix_expression()}"
    nix.evaluate_expression(expression)


@nix
def test_fetch_content_equals_file_content_from_nix_expression(
    network_file: NetworkFile, nix: Nix
):
    fetch_content = network_file.fetch()

    nix_expression = "with builtins;"
    nix_expression += "let pkgs = import <nixpkgs> {};"
    nix_expression += f"fileContent = readFile ({network_file.nix_expression()});"
    nix_expression += " in "
    nix_expression += 'pkgs.writeTextFile { name = "test"; text = fileContent; }'
    with tempfile.TemporaryDirectory() as target_directory:
        target_file = os.path.join(target_directory, "result")
        nix.build_expression(nix_expression, out_link=target_file)
        with open(target_file) as f:
            nix_content = f.read()
    assert nix_content == fetch_content


@pytest.fixture(params=["url", "git", "disk"])
def network_file(logger: Logger, request, data_directory):
    if request.param == "url":
        return UrlTextFile(
            url="https://raw.githubusercontent.com/nix-community/pypi2nix/6fe6265b62b53377b4677a39c6ee48550c1f2186/.gitignore",
            logger=logger,
            name="testname",
        )
    elif request.param == "disk":
        return DiskTextFile(path=os.path.join(data_directory, "test.txt"),)
    else:
        repository_url = "https://github.com/nix-community/pypi2nix.git"
        path = ".gitignore"
        revision_name = "e56cbbce0812359e80ced3d860e1f232323b2976"
        return GitTextFile(
            repository_url=repository_url,
            revision_name=revision_name,
            path=path,
            logger=logger,
        )
