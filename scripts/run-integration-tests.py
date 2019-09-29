#!/usr/bin/env python

import os
import subprocess

from repository import ROOT


def main():
    files = (
        os.path.join(ROOT, "integrationtests", name)
        for name in os.listdir(os.path.join(ROOT, "integrationtests"))
        if name.startswith("test_") and name.endswith(".py")
    )
    for path in files:
        subprocess.run(["python", "-m", "unittest", path], check=True)


if __name__ == "__main__":
    main()
