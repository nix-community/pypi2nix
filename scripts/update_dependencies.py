#!/usr/bin/env python

import subprocess

from repository import ROOT


def main():
    subprocess.run(["nix", "build"], cwd=ROOT, check=True)
    subprocess.run(
        [
            "result/bin/pypi2nix",
            "-r",
            "requirements.txt",
            "-r",
            "requirements-dev.txt",
            "--no-default-overrides",
        ],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
