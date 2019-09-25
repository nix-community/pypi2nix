import os.path

with open(os.path.join(os.path.dirname(__file__), "VERSION")) as f:
    pypi2nix_version = f.read().strip()
