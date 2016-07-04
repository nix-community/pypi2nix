
SENTRY_BUILD_INPUTS="libxslt libxml2 zlib libffi openssl postgresql freetype libjpeg zlib libtiff libwebp tcl lcms2"
LEKTOR_BUILD_INPUTS="libffi openssl unzip"
PYPI2NIX=../result/bin/pypi2nix


all: sentry empy lektor rss2email awscli

clear: sentry-clear empy-clear lektor-clear rss2email-clear

pypi2nix-clear:
	@rm -f ../result

$(PYPI2NIX): pypi2nix-clear
	@echo "building pypi2nix ..."
	@ cd .. && nix-build release.nix -A build.x86_64-linux 

sentry: sentry.nix
	@echo "building and testing sentry ..."
	@nix-build sentry.nix -o sentry -A interpreter --show-trace
	@./sentry/bin/python -c 'import sentry'
	@./sentry/bin/sentry --help
	@nix-shell sentry.nix -A interpreter --run "python -c 'import sentry'"
	@nix-shell sentry.nix -A interpreter --run "sentry --help"

sentry.nix: sentry.txt $(PYPI2NIX)
	@echo "generating sentry nix expressions ..."
	@$(PYPI2NIX) -r sentry.txt -E $(SENTRY_BUILD_INPUTS) -I $(NIX_PATH)

sentry.txt: sentry-clear
	@echo "Sentry==8.5.1" >> sentry.txt

sentry-clear:
	@rm -f sentry
	@rm -f sentry.txt
	@rm -f sentry.nix
	@rm -f sentry_generated.nix


empy: empy.nix
	@echo "building and testing empy ..."
	@nix-build empy.nix -o empy -A interpreter --show-trace
	@./empy/bin/python -c 'import em'
	@nix-shell empy.nix -A interpreter --run "python -c 'import em'"

empy.nix: empy.txt $(PYPI2NIX)
	@echo "generating empy nix expressions ..."
	@$(PYPI2NIX) -r empy.txt -I $(NIX_PATH)

empy.txt: empy-clear
	@echo "empy" > empy.txt

empy-clear:
	@rm -f empy
	@rm -f empy.txt
	@rm -f empy.nix
	@rm -f empy_generated.nix


lektor: lektor.nix
	@echo "building and testing lektor ..."
	@nix-build lektor.nix -o lektor -A interpreter --show-trace
	@./lektor/bin/python -c 'import lektor'
	@./lektor/bin/lektor --help
	@nix-shell lektor.nix -A interpreter --run "python -c 'import lektor'"
	@nix-shell lektor.nix -A interpreter --run "lektor --help"

lektor.nix: lektor.txt $(PYPI2NIX)
	@echo "generating lektor nix expressions ..."
	@$(PYPI2NIX) -r lektor.txt -E $(LEKTOR_BUILD_INPUTS) -I $(NIX_PATH)

lektor.txt: lektor-clear
	@echo "Lektor" > lektor.txt

lektor-clear:
	@rm -f lektor
	@rm -f lektor.txt
	@rm -f lektor.nix
	@rm -f lektor_generated.nix


rss2email: rss2email.nix
	@echo "building and testing rss2email ..."
	@nix-build rss2email.nix -o rss2email -A interpreter --show-trace
	@./rss2email/bin/python3 -c 'import rss2email'
	@./rss2email/bin/r2e --help
	@nix-build rss2email.nix -A interpreter --run "python3 -c 'import rss2email'"
	@nix-build rss2email.nix -A interpreter --run "r2e --help"

rss2email.nix: rss2email.txt $(PYPI2NIX)
	@echo "generating rss2email nix expressions ..."
	@$(PYPI2NIX) -r rss2email.txt -V "3.4" -I $(NIX_PATH)

rss2email.txt: rss2email-clear
	@echo "https://github.com/wking/rss2email/archive/master.zip" > rss2email.txt

rss2email-clear:
	@rm -f rss2email
	@rm -f rss2email.txt
	@rm -f rss2email.nix
	@rm -f rss2email_generated.nix



awscli: awscli.nix
	@echo "building and testing awscli ..."
	@nix-build awscli.nix -o awscli -A interpreter --show-trace
	@./awscli/bin/python -c 'import awscli'
	@PAGER=none ./awscli/bin/aws help
	@nix-shell awscli.nix -A interpreter --run "python -c 'import awscli'"
	@nix-shell awscli.nix -A interpreter --run "PAGER=none aws help"

awscli.nix: awscli.txt $(PYPI2NIX)
	@echo "generating awscli nix expressions ..."
	@$(PYPI2NIX) -r awscli.txt -I $(NIX_PATH)

awscli.txt: awscli-clear
	@echo "awscli" > awscli.txt

awscli-clear:
	@rm -f awscli
	@rm -f awscli.txt
	@rm -f awscli.nix
	@rm -f awscli_generated.nix
