
NIX_PATH=
SENTRY_BUILD_INPUTS="libxslt libxml2 zlib libffi openssl postgresql"

all: sentry

sentry: sentry.nix

sentry.nix: sentry.txt
	which pypi2nix
	pypi2nix sentry.txt -E $(SENTRY_BUILD_INPUTS)

sentry.txt:
	nix-shell \
		-p pythonPackages.virtualenv $(SENTRY_BUILD_INPUTS) \
	    --command "\
		    virtualenv sentry;\
			sentry/bin/pip install -U sentry;\
			sentry/bin/pip freeze > sentry.txt;\
			" \
		-I nixpkgs=/home/rok/dev/nixos/nixpkgs
	
