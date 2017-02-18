flakes:
	nix-shell '<nixpkgs>' -p python3Packages.flake8 --command \
		'flake8 src/ --ignore E501'

.PHONY: flakes
