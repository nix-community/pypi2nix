flakes:
	nix-shell '<nixpkgs>' -p python3Packages.flake8 --command \
		'flake8 src/ --ignore E501'

python-env:
	pypi2nix \
		-e click \
		-e requests \
		-e jinja2 \
		-V 3 \
		--default-overrides

.PHONY: flakes
