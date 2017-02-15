OS := $(shell uname)
PYPI2NIX=../result/bin/pypi2nix
NIX_PATH=nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixpkgs-unstable.tar.gz


ifeq ($(OS), Darwin)
LEKTOR_BUILD_INPUTS="libffi openssl unzip darwin.apple_sdk.frameworks.Security darwin.apple_sdk.frameworks.CoreServices darwin.cf-private"
else
LEKTOR_BUILD_INPUTS="libffi openssl unzip"
endif

.PHONY: \
	awscli_and_requests \
	empy \
	ldap \
	lektor \
	mercurial \
	rss2email \
	scipy \
	pillow \
	tornado \
	vulnix

all: \
	awscli_and_requests \
	empy \
	ldap \
	lektor \
	mercurial \
	rss2email \
	scipy \
	pillow \
	tornado \
	vulnix

clear: \
	awscli_and_requests-clear \
	empy-clear \
	ldap-clear \
	lektor-clear \
	mercurial-clear \
	pypi2nix-clear \
	rss2email-clear \
	scipy-clear \
	pillow-clear \
	tornado-clear \
	vulnix-clear


pypi2nix-clear:
	rm -f ../result

$(PYPI2NIX): pypi2nix-clear
	echo "building pypi2nix ..."
	cd .. && nix-build release.nix -A build.x86_64-linux

pillow: pillow.nix
	echo "building and testing pillow..."
	nix-build pillow.nix -o pillow -A interpreter --show-trace &> /dev/null
	./pillow/bin/python -c 'import PIL'
	nix-shell pillow.nix -A interpreter --run "python -c 'import PIL'" 

pillow.nix: pillow.txt $(PYPI2NIX)
	echo "generating pillownix expressions ..."
	$(PYPI2NIX) \
		-v \
		-V "3.5" \
		--basename pillow \
		-r pillow.txt \
		-E "pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl" \
		-I $(NIX_PATH)

pillow.txt: pillow-clear
	echo "Pillow" > pillow.txt

pillow-clear:
	rm -f pillow
	rm -f pillow.txt
	rm -f pillow.nix
	rm -f pillow_generated.nix
	rm -f pillow_frozen.txt


empy: empy.nix
	echo "building and testing empy ..."
	nix-build empy.nix -o empy -A interpreter --show-trace
	./empy/bin/python -c 'import em'
	nix-shell empy.nix -A interpreter --run "python -c 'import em'"

empy.nix: empy.txt $(PYPI2NIX)
	echo "generating empy nix expressions ..."
	$(PYPI2NIX) \
		-v \
		-V "2.7" \
		--basename empy \
		-r empy.txt \
		-I $(NIX_PATH) \

empy.txt: empy-clear
	echo "empy" > empy.txt

empy-clear:
	rm -f empy
	rm -f empy.txt
	rm -f empy.nix
	rm -f empy_generated.nix
	rm -f empy_frozen.txt


lektor: lektor.nix
	echo "building and testing lektor ..."
	nix-build lektor.nix -o lektor -A interpreter --show-trace
	./lektor/bin/python -c 'import lektor'
	./lektor/bin/lektor --help
	nix-shell lektor.nix -A interpreter --run "python -c 'import lektor'"
	nix-shell lektor.nix -A interpreter --run "lektor --help"

lektor.nix: lektor.txt $(PYPI2NIX)
	echo "generating lektor nix expressions ..."
	$(PYPI2NIX) \
		-v \
		-V "2.7" \
		--basename lektor \
		--setup-requires "six packaging appdirs" \
		-r lektor.txt \
		-E $(LEKTOR_BUILD_INPUTS) \
		-I $(NIX_PATH)

lektor.txt: lektor-clear
	echo "Lektor" > lektor.txt

lektor-clear:
	rm -f lektor
	rm -f lektor.txt
	rm -f lektor.nix
	rm -f lektor_generated.nix
	rm -f lektor_frozen.txt



rss2email: rss2email.nix
	echo "building and testing rss2email ..."
	nix-build rss2email.nix -o rss2email -A interpreter --show-trace
	./rss2email/bin/python -c 'import rss2email'
	./rss2email/bin/r2e --help
	nix-build rss2email.nix -A interpreter --run "python -c 'import rss2email'"
	nix-build rss2email.nix -A interpreter --run "r2e --help"

rss2email.nix: rss2email.txt $(PYPI2NIX)
	echo "generating rss2email nix expressions ..."
	$(PYPI2NIX) \
		-v \
		--setup-requires "six packaging appdirs" \
		--basename rss2email \
		-r rss2email.txt -V "3.4" \
		-I $(NIX_PATH)

rss2email.txt: rss2email-clear
	echo "https://github.com/wking/rss2email/archive/master.zip#egg=rss2email" > rss2email.txt

rss2email-clear:
	rm -f rss2email
	rm -f rss2email.txt
	rm -f rss2email.nix
	rm -f rss2email_generated.nix
	rm -f rss2email_frozen.txt



awscli_and_requests: awscli_and_requests.nix
	echo "building and testing awscli and requests library ..."
	nix-build awscli.nix -o awscli_and_requests -A interpreter --show-trace
	./awscli_and_requests/bin/python -c 'import awscli; import requests'
	PAGER=none ./awscli_and_requests/bin/aws help
	nix-shell awscli.nix -A interpreter --run "python -c 'import awscli'"
	nix-shell awscli.nix -A interpreter --run "python -c 'import awscli; import requests'"
	nix-shell awscli.nix -A interpreter --run "PAGER=none aws help"

awscli_and_requests.nix: awscli_and_requests.txt $(PYPI2NIX)
	echo "generating awscli and requests nix expressions ..."
	$(PYPI2NIX) -v --basename awscli -r awscli.txt -r requests.txt -I $(NIX_PATH) -V "2.7"

awscli_and_requests.txt: awscli_and_requests-clear
	echo "awscli" > awscli.txt
	echo "requests" > requests.txt

awscli_and_requests-clear:
	rm -f awscli_and_requests
	rm -f awscli.txt
	rm -f requests.txt
	rm -f awscli_and_requests.nix
	rm -f awscli_and_requests_generated.nix
	rm -f awscli_and_requests_frozen.txt



vulnix: vulnix-clear $(PYPI2NIX)
	echo "building and testing vulnix..."
	git clone https://github.com/garbas/vulnix vulnix-src
	cd vulnix-src && nix-shell update.nix --argstr pypi2nix "./../$(PYPI2NIX)"
	NIX_PATH=$(NIX_PATH) nix-build vulnix-src/default.nix --arg pkgs "import <nixpkgs> {}" -o vulnix
	./vulnix/bin/vulnix --help

vulnix-clear:
	rm -f vulnix
	rm -rf vulnix-src


scipy: scipy.nix
	echo "building and testing scipy..."
	nix-build scipy.nix -o scipy -A interpreter --show-trace
	./scipy/bin/python -c 'import scipy'
	nix-shell scipy.nix -A interpreter --run "python -c 'import scipy'"

scipy.nix: scipy.txt $(PYPI2NIX)
	echo "generating scipy.nix expressions ..."
	$(PYPI2NIX) -v --basename scipy -r scipy.txt -s numpy -E gfortran -E blas -I $(NIX_PATH) -V "3.5"

scipy.txt: scipy-clear
	echo "scipy" > scipy.txt
	echo "numpy" >> scipy.txt

scipy-clear:
	rm -f scipy
	rm -f scipy.txt
	rm -f scipy.nix
	rm -f scipy_generated.nix
	rm -f scipy_frozen.txt

tornado: tornado.nix
	echo "building and testing tornado..."
	nix-build tornado.nix -o tornado -A interpreter --show-trace
	./tornado/bin/python -c 'import tornado'
	nix-shell tornado.nix -A interpreter --run "python -c 'import tornado'"
	if [ `cat tornado_generated.nix | grep "69253c820df473407c562a227d0ba36df25018ab" | wc -l` != "1" ]; then \
			echo "ERROR: Revision '69253c820df473407c562a227d0ba36df25018ab' not found in tornado_generated.nix!"; \
			exit 123; \
		fi

tornado.nix: tornado.txt $(PYPI2NIX)
	echo "generating tornado.nix expressions ..."
	$(PYPI2NIX) -v --basename tornado -r tornado.txt -I $(NIX_PATH) -V "3.5"

tornado.txt: tornado-clear
	echo "-e git+git://github.com/tornadoweb/tornado.git@69253c820df473407c562a227d0ba36df25018ab#egg=tornado" > tornado.txt

tornado-clear:
	rm -f tornado
	rm -f tornado.txt
	rm -f tornado.nix
	rm -f tornado_generated.nix
	rm -f tornado_frozen.txt


ldap: ldap.nix
	echo "building and testing ldap..."
	nix-build ldap.nix -o ldap -A interpreter --show-trace
	./ldap/bin/python -c 'import ldap'
	nix-shell ldap.nix -A interpreter --run "python -c 'import ldap'"

ldap.nix: ldap.txt $(PYPI2NIX)
	echo "generating ldap.nix expressions ..."
	$(PYPI2NIX) \
		-v \
		--basename ldap \
		-N "NIX_CFLAGS_COMPILE=\"-I\$${pkgs.cyrus_sasl.dev}/include/sasl \$$NIX_CFLAGS_COMPILE\"" \
		-E "openldap cyrus_sasl openssl" \
		--setup-requires "six packaging appdirs" \
		-r ldap.txt \
		-I $(NIX_PATH) \
		-V "2.7"

ldap.txt: ldap-clear
	echo "python-ldap" > ldap.txt

ldap-clear:
	rm -f ldap
	rm -f ldap.txt
	rm -f ldap.nix
	rm -f ldap_generated.nix
	rm -f ldap_frozen.txt


mercurial: mercurial.nix
	echo "building and testing mercurial..."
	nix-build mercurial.nix -o mercurial -A interpreter --show-trace -j 1
	./mercurial/bin/python -c 'import flake8'
	nix-shell mercurial.nix -A interpreter --run "python -c 'import flake8'"
	if [ `cat mercurial_generated.nix | grep "a209fb6" | wc -l` != "1" ]; then \
			echo "ERROR: Revision 'a209fb6' not found in tornado_generated.nix!"; \
			exit 123; \
		fi

mercurial.nix: mercurial.txt $(PYPI2NIX)
	echo "generating mercurial.nix expressions ..."
	$(PYPI2NIX) -v --basename mercurial -r mercurial.txt -I $(NIX_PATH) -V "2.7" -E "mercurial"


mercurial.txt: mercurial-clear
	echo "-e hg+https://bitbucket.org/tarek/flake8@a209fb6#egg=flake8" > mercurial.txt
	echo "pytest-runner" >> mercurial.txt
	echo "setuptools-scm" >> mercurial.txt

mercurial-clear:
	rm -f mercurial
	rm -f mercurial.txt
	rm -f mercurial.nix
	rm -f mercurial_generated.nix
	rm -f mercurial_frozen.txt
