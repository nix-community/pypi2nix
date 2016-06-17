
SENTRY_BUILD_INPUTS="libxslt libxml2 zlib libffi openssl postgresql freetype libjpeg zlib libtiff libwebp tcl lcms2"
LEKTOR_BUILD_INPUTS="libffi openssl unzip"
PYPI2NIX=pypi2nix


all: sentry empy lektor rss2email awscli

clear: sentry-clear empy-clear lektor-clear rss2email-clear


sentry: sentry.nix
	nix-build sentry.nix -A sentry -o sentry

sentry.nix: sentry.txt
	$(PYPI2NIX) -r sentry.txt -E $(SENTRY_BUILD_INPUTS) -I $(NIX_PATH)

sentry.txt: sentry-clear
	echo "Sentry" >> sentry.txt

sentry-clear:
	rm -f sentry
	rm -f sentry.txt
	rm -f sentry.nix
	rm -f sentry_generated.nix


empy: empy.nix
	nix-build empy.nix -A empy -o empy

empy.nix: empy.txt
	$(PYPI2NIX) -r empy.txt -I $(NIX_PATH)

empy.txt: empy-clear
	echo "empy" > empy.txt

empy-clear:
	rm -f empy
	rm -f empy.txt
	rm -f empy.nix
	rm -f empy_generated.nix


lektor: lektor.nix
	nix-build lektor.nix -A Lektor -o lektor

lektor.nix: lektor.txt
	$(PYPI2NIX) -r lektor.txt -E $(LEKTOR_BUILD_INPUTS) -I $(NIX_PATH)

lektor.txt: lektor-clear
	echo "Lektor" > lektor.txt

lektor-clear:
	rm -f lektor
	rm -f lektor.txt
	rm -f lektor.nix
	rm -f lektor_generated.nix


rss2email: rss2email.nix
	nix-build rss2email.nix -A rss2email -o rss2email

rss2email.nix: rss2email.txt
	$(PYPI2NIX) -r rss2email.txt -V "3.4" -I $(NIX_PATH)

rss2email.txt: rss2email-clear
	echo "https://github.com/wking/rss2email/archive/master.zip" > rss2email.txt

rss2email-clear:
	rm -f rss2email
	rm -f rss2email.txt
	rm -f rss2email.nix
	rm -f rss2email_generated.nix



awscli: awscli.nix
	nix-build awscli.nix -A awscli -o awscli

awscli.nix: awscli.txt
	$(PYPI2NIX) -r awscli.txt -I $(NIX_PATH)

awscli.txt: awscli-clear
	echo "awscli" > awscli.txt

awscli-clear:
	rm -f awscli
	rm -f awscli.txt
	rm -f awscli.nix
	rm -f awscli_generated.nix


