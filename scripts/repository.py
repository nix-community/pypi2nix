from pypi2nix.path import Path


def find_root(start: Path = Path(".")) -> Path:
    absolute_location = start.resolve()
    if (absolute_location / ".git").is_directory():
        return absolute_location
    else:
        return find_root(absolute_location / "..")


ROOT = find_root()
