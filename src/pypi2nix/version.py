import os.path

HERE = os.path.dirname(__file__)
VERSION_FILE = os.path.join(HERE, "VERSION")
with open(VERSION_FILE) as handle:
    pypi2nix_version = handle.read().strip()
