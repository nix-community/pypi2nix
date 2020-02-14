from typing import Optional

from pypi2nix.logger import Logger
from pypi2nix.pypi import Pypi
from pypi2nix.utils import prefetch_git
from pypi2nix.wheels import Index


class PackageSource:
    def __init__(self, index: Index, pypi: Pypi, logger: Logger):
        self.index = index
        self.pypi = pypi
        self.logger = logger

    def update_package_from_master(self, package_name: str) -> None:
        url = self._get_url_for_package(package_name)
        if url is None:
            self._log_no_update_warning(package_name)
            return
        repo_data = prefetch_git(url)
        self.index[package_name] = Index.GitEntry(
            url=repo_data["url"], rev=repo_data["rev"], sha256=repo_data["sha256"],
        )
        self._log_update_success(package_name)

    def update_package_from_pip(self, package_name: str) -> None:
        package = self.pypi.get_package(package_name)
        source_release = self.pypi.get_source_release(
            name=package_name, version=package.version
        )
        if source_release is None:
            self._log_no_update_warning(package_name)
            return
        self.index[package_name] = Index.UrlEntry(
            url=source_release.url, sha256=source_release.sha256_digest
        )
        self._log_update_success(package_name)

    def _get_url_for_package(self, package_name: str) -> Optional[str]:
        return SOURCE_BY_PACKAGE_NAME.get(package_name)

    def _log_no_update_warning(self, package_name: str) -> None:
        self.logger.warning(f"Could not update source for package `{package_name}`")

    def _log_update_success(self, package_name: str) -> None:
        self.logger.info(f"Successfully updated package `{package_name}`")


SOURCE_BY_PACKAGE_NAME = {"pip": "https://github.com/pypa/pip.git"}
