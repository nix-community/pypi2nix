import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from attr import attrib
from attr import attrs

from pypi2nix.archive import Archive
from pypi2nix.logger import Logger
from pypi2nix.requirement_parser import RequirementParser
from pypi2nix.source_distribution import SourceDistribution

from .templates import render_template


@attrs
class PackageGenerator:
    """Generate source distributions on for testing

    This class aims to provide an easy to use way of generating test
    data.  Since pypi2nix deals a lot with python packages it is
    necessary have python packages available for testing.
    """

    _target_directory: Path = attrib()
    _requirement_parser: RequirementParser = attrib()
    _logger: Logger = attrib()

    def generate_setuptools_package(
        self, name: str, version: str = "1.0", install_requires: List[str] = []
    ) -> SourceDistribution:
        with TemporaryDirectory() as directory_path_string:
            build_directory: Path = Path(directory_path_string)
            self._generate_setup_py(build_directory, name=name, version=version)
            self._generate_setup_cfg(
                build_directory,
                name=name,
                version=version,
                install_requires=install_requires,
            )
            built_distribution_archive = self._build_package(
                build_directory=build_directory, name=name, version=version
            )
            source_distribution = SourceDistribution.from_archive(
                built_distribution_archive,
                logger=self._logger,
                requirement_parser=self._requirement_parser,
            )
            self._move_package_target_directory(built_distribution_archive)
        return source_distribution

    def _generate_setup_py(
        self, target_directory: Path, name: str, version: str
    ) -> None:
        content = render_template(Path("setup.py"), context={},)
        (target_directory / "setup.py").write_text(content)

    def _generate_setup_cfg(
        self,
        target_directory: Path,
        name: str,
        version: str,
        install_requires: List[str],
    ) -> None:
        content = render_template(
            Path("setup.cfg"),
            context={
                "name": name,
                "version": version,
                "install_requires": install_requires,
            },
        )
        (target_directory / "setup.cfg").write_text(content)

    def _build_package(self, build_directory: Path, name: str, version: str) -> Archive:
        subprocess.run(
            ["python", "setup.py", "sdist"], cwd=str(build_directory), check=True
        )
        tar_gz_path = build_directory / "dist" / f"{name}-{version}.tar.gz"
        return Archive(path=str(tar_gz_path))

    def _move_package_target_directory(self, distribution_archive: Archive) -> None:
        shutil.copy(distribution_archive.path, self._target_directory)
