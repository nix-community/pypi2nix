
NIX_PATH=
SENTRY_BUILD_INPUTS="libxslt libxml2 zlib libffi openssl postgresql"

all: sentry empy

sentry: sentry.nix

sentry.nix: sentry.txt
	pypi2nix sentry.txt -E $(SENTRY_BUILD_INPUTS)

sentry.txt:
	nix-shell \
		-p pythonPackages.virtualenv $(SENTRY_BUILD_INPUTS) \
	    --command "\
		    virtualenv sentry;\
			sentry/bin/pip install -U sentry;\
			sentry/bin/pip freeze > sentry.txt;\
			"

empy: empy.nix

empy.nix: empy.txt
	pypi2nix -r empy.txt -I $(NIX_PATH)

empy.txt:
	nix-shell \
		-p pythonPackages.virtualenv \
	    --command "\
		    virtualenv empy;\
			empy/bin/pip install -U empy;\
			empy/bin/pip freeze > empy.txt;\
			"\
		-I $(NIX_PATH)
	chmod 777 empy.txt
