from abc import ABCMeta
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from urllib.parse import urlparse

from attr import attrib
from attr import attrs
from attr import evolve
from packaging.utils import canonicalize_name

from pypi2nix.environment_marker import EnvironmentMarker
from pypi2nix.environment_marker import MarkerEvaluationFailed
from pypi2nix.logger import Logger
from pypi2nix.package_source import GitSource
from pypi2nix.package_source import HgSource
from pypi2nix.package_source import PackageSource
from pypi2nix.package_source import PathSource
from pypi2nix.package_source import UrlSource
from pypi2nix.target_platform import TargetPlatform


class IncompatibleRequirements(Exception):
    pass


class Requirement(metaclass=ABCMeta):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def extras(self) -> Set[str]:
        pass

    @abstractmethod
    def add(
        self, other: "Requirement", target_platform: TargetPlatform
    ) -> "Requirement":
        pass

    @abstractmethod
    def source(self) -> Optional[PackageSource]:
        pass

    @abstractmethod
    def environment_markers(self) -> Optional[EnvironmentMarker]:
        pass

    @abstractmethod
    def logger(self) -> Logger:
        pass

    def applies_to_target(
        self, target_platform: TargetPlatform, extras: List[str] = []
    ) -> bool:
        environment_markers = self.environment_markers()
        try:
            return (
                True
                if environment_markers is None
                else environment_markers.applies_to_platform(target_platform, extras)
            )
        except MarkerEvaluationFailed as e:
            self.logger().warning(
                "Could not evaluate environment marker `{marker}`. Error message was `{message}`".format(
                    marker=environment_markers, message=e.args
                )
            )
            return False

    @abstractmethod
    def to_line(self) -> str:
        pass


@attrs
class UrlRequirement(Requirement):
    _name: str = attrib()
    _url: str = attrib()
    _extras: Set[str] = attrib()
    _environment_markers: Optional[EnvironmentMarker] = attrib()
    _logger: Logger = attrib()

    def name(self) -> str:
        return canonicalize_name(self._name)

    def extras(self) -> Set[str]:
        return self._extras

    def logger(self) -> Logger:
        return self._logger

    def add(self, other: Requirement, target_platform: TargetPlatform) -> Requirement:
        if not self.applies_to_target(target_platform):
            return other
        elif not other.applies_to_target(target_platform):
            return self
        elif self.name() != other.name():
            raise IncompatibleRequirements(
                "Cannot add requirments with different names `{name1}` and `{name2}`".format(
                    name1=self.name(), name2=other.name()
                )
            )
        else:
            if isinstance(other, VersionRequirement):
                return self
            elif isinstance(other, PathRequirement):
                raise IncompatibleRequirements(
                    "Cannot combine requirements with with url `{url}` and path `{path}`".format(
                        url=self.url, path=other.path
                    )
                )
            elif isinstance(other, UrlRequirement):
                if self.url != other.url:
                    raise IncompatibleRequirements(
                        "Cannot combine requirements with different urls `{url1}` and `{url2}`".format(
                            url1=self.url, url2=other.url
                        )
                    )
                else:
                    return self
            else:
                raise IncompatibleRequirements(
                    "Did not recognize requirement type of {}".format(other)
                )

    def source(self) -> PackageSource:
        if self._url.startswith("git+"):
            return self._handle_git_source(self._url[4:])
        elif self._url.startswith("git://"):
            return self._handle_git_source(self._url)
        elif self._url.startswith("hg+"):
            return self._handle_hg_source(self._url[3:])
        elif self.url_scheme() == "file":
            return PathSource(path=self.url_path())
        else:
            return UrlSource(url=self._url, logger=self._logger)

    def environment_markers(self) -> Optional[EnvironmentMarker]:
        return self._environment_markers

    def _handle_hg_source(self, url: str) -> HgSource:
        try:
            url, rev = url.split("@")
        except ValueError:
            return HgSource(url=url, logger=self._logger)
        else:
            return HgSource(url=url, revision=rev, logger=self._logger)

    def _handle_git_source(self, url: str) -> GitSource:
        try:
            url, rev = url.split("@")
        except ValueError:
            return GitSource(url=url)
        else:
            return GitSource(url=url, revision=rev)

    def to_line(self) -> str:
        extras = "[" + ",".join(self.extras()) + "]" if self.extras() else ""
        return "{url}#egg={name}{extras}".format(
            url=self._url, name=self.name(), extras=extras
        )

    def url(self) -> str:
        return self._url

    def url_scheme(self) -> str:
        url = urlparse(self.url())
        return url.scheme

    def url_path(self) -> str:
        url = urlparse(self.url())
        return url.path


@attrs
class PathRequirement(Requirement):
    _name: str = attrib()
    _path: str = attrib()
    _extras: Set[str] = attrib()
    _environment_markers: Optional[EnvironmentMarker] = attrib()
    _logger: Logger = attrib()

    def name(self) -> str:
        return canonicalize_name(self._name)

    def extras(self) -> Set[str]:
        return self._extras

    def logger(self) -> Logger:
        return self._logger

    def add(self, other: Requirement, target_platform: TargetPlatform) -> Requirement:
        if not self.applies_to_target(target_platform):
            return other
        elif not other.applies_to_target(target_platform):
            return self
        elif self.name() != other.name():
            raise IncompatibleRequirements(
                "Cannot add requirements with different names `{name1}` and `{name2}`".format(
                    name1=self.name(), name2=other.name()
                )
            )
        else:
            if isinstance(other, VersionRequirement):
                return self
            elif isinstance(other, UrlRequirement):
                raise IncompatibleRequirements(
                    "Cannot combine requirements with path `{path} and url `{url}`".format(
                        path=self.path, url=other.url
                    )
                )
            elif isinstance(other, PathRequirement):
                if self.path != other.path:
                    raise IncompatibleRequirements(
                        "Cannot combine requirements with different paths `{path1}` and `{path2}`".format(
                            path1=self.path, path2=other.path
                        )
                    )
                else:
                    return self
            else:
                raise IncompatibleRequirements(
                    "Did not recognize requirement type of {}".format(other)
                )

    def source(self) -> PathSource:
        return PathSource(path=self._path)

    def environment_markers(self) -> Optional[EnvironmentMarker]:
        return self._environment_markers

    def to_line(self) -> str:
        extras = "[" + ",".join(self.extras()) + "]" if self.extras() else ""
        return "file://{path}#egg={name}{extras}".format(
            path=self._path, extras=extras, name=self.name()
        )

    def path(self) -> str:
        return self._path

    def change_path(self, mapping: Callable[[str], str]) -> "PathRequirement":
        return evolve(self, path=mapping(self._path))


@attrs
class VersionRequirement(Requirement):
    _name: str = attrib()
    _versions: List[Tuple[str, str]] = attrib()
    _extras: Set[str] = attrib()
    _environment_markers: Optional[EnvironmentMarker] = attrib()
    _logger: Logger = attrib()

    def name(self) -> str:
        return canonicalize_name(self._name)

    def extras(self) -> Set[str]:
        return self._extras

    def logger(self) -> Logger:
        return self._logger

    def add(self, other: Requirement, target_platform: TargetPlatform) -> Requirement:
        if not self.applies_to_target(target_platform):
            return other
        elif not other.applies_to_target(target_platform):
            return self
        elif self.name() != other.name():
            raise IncompatibleRequirements(
                "Cannot add requirments with different names `{name1}` and `{name2}`".format(
                    name1=self.name(), name2=other.name()
                )
            )
        else:
            if isinstance(other, PathRequirement):
                return other
            elif isinstance(other, UrlRequirement):
                return other
            elif isinstance(other, VersionRequirement):
                return VersionRequirement(
                    name=self.name(),
                    extras=self._extras.union(other._extras),
                    versions=self.version() + other.version(),
                    environment_markers=None,
                    logger=self.logger(),
                )
            else:
                raise IncompatibleRequirements(
                    "Did not recognize requirement type of {}".format(other)
                )

    def source(self) -> None:
        return None

    def environment_markers(self) -> Optional[EnvironmentMarker]:
        return self._environment_markers

    def version(self) -> List[Tuple[str, str]]:
        return self._versions

    def to_line(self) -> str:
        version = ", ".join(
            [
                "{operator} {specifier}".format(operator=operator, specifier=specifier)
                for operator, specifier in self._versions
            ]
        )
        extras = (
            "[{extras}]".format(extras=",".join(self.extras())) if self.extras() else ""
        )
        return "{name}{extras} {version}".format(
            name=self._name, version=version, extras=extras
        )
