
SENTRY_BUILD_INPUTS="libxslt libxml2 zlib libffi openssl postgresql"
LEKTOR_BUILD_INPUTS="libffi openssl unzip"


all: sentry empy lektor

clear: sentry-clear empy-clear lektor-clear


sentry: sentry.nix

sentry.nix: sentry.txt
	pypi2nix -r sentry.txt -E $(SENTRY_BUILD_INPUTS) -I $(NIX_PATH)

sentry.txt: sentry-clear
	echo "Sentry" > sentry.txt

sentry-clear:
	rm -f sentry.*
	rm -f sentry_generated.nix


empy: empy.nix

empy.nix: empy.txt
	pypi2nix -r empy.txt -I $(NIX_PATH)

empy.txt: empy-clear
	echo "empy" > empy.txt

empy-clear:
	rm -f empy.*
	rm -f empy_generated.nix


lektor: lektor.nix

lektor.nix: lektor.txt
	pypi2nix -r lektor.txt -E $(LEKTOR_BUILD_INPUTS) -I $(NIX_PATH)

lektor.txt: lektor-clear
	echo "Lektor" > lektor.txt

lektor-clear:
	rm -f lektor.*
	rm -f lektor_generated.nix
