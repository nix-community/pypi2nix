#!/usr/bin/env python

import os
import subprocess

from repository import ROOT


def run_tests_from_file(path: str) -> None:
    subprocess.run(["python", "-m", "unittest", path, '-k', 'TestCase'], check=True)


def main():
    files = (
        os.path.join(ROOT, "integrationtests", name)
        for name in os.listdir(os.path.join(ROOT, "integrationtests"))
        if name.startswith("test_") and name.endswith(".py")
    )
    for path in files:
        run_tests_from_file(path)


if __name__ == "__main__":
    main()
