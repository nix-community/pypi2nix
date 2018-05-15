#!/usr/bin/env sh

set -e

nix-shell packages_with_util.nix -A flake8 --run 'python -c "import flake8"'
! nix-shell packages_with_util.nix -A flake8 --run 'python -c "import tornado"'

nix-shell packages_with_util.nix -A tornado --run 'python -c "import tornado"'
! nix-shell packages_with_util.nix -A tornado --run 'python -c "import flake8"'
