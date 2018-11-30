OS := $(shell uname)
PYPI2NIX=./pypi2nix/bin/pypi2nix
NIX_PATH=nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixpkgs-unstable.tar.gz
NIX_BUILD=nix build -f
NIX_SHELL=nix run -f
AFTER=


ifeq ($(OS), Darwin)
LEKTOR_BUILD_INPUTS="libffi openssl unzip darwin.apple_sdk.frameworks.Security darwin.apple_sdk.frameworks.CoreServices darwin.cf-private"
else
LEKTOR_BUILD_INPUTS="libffi openssl unzip"
endif


.PHONY: \
	aiohttp \
	awscli_and_requests \
	connexion \
	empy \
	flake8 \
	ldap \
	lektor \
	mercurial \
	pillow \
	rss2email \
	scipy \
	tornado \
	packages_with

all: \
	aiohttp \
	awscli_and_requests \
	connexion \
	empy \
	flake8 \
	ldap \
	lektor \
	mercurial \
	pillow \
	rss2email \
	scipy \
	tornado \
	packages_with

clear: \
	aiohttp-clear \
	awscli_and_requests-clear \
	connexion-clear \
	empy-clear \
	flake8-clear \
	ldap-clear \
	lektor-clear \
	mercurial-clear \
	pillow-clear \
	pypi2nix-clear \
	rss2email-clear \
	scipy-clear \
	tornado-clear \
	packages_with-clear


pypi2nix-clear:
	rm -f pypi2nix

$(PYPI2NIX): pypi2nix-clear
	echo "building pypi2nix ..."
	$(NIX_BUILD) ../ -I $(NIX_PATH) -o pypi2nix



#------------------------------------------------------------------------------


aiohttp: aiohttp.nix
	echo "building and testing aiohttp..."
	$(NIX_BUILD) aiohttp.nix -o aiohttp interpreter $(AFTER)
	./aiohttp/bin/python -c 'import aiohttp'
	$(NIX_SHELL) aiohttp.nix interpreter --command python -c 'import aiohttp'

aiohttp.nix: aiohttp.txt $(PYPI2NIX)
	echo "generating aiohttp.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.5" \
		--basename aiohttp \
		-r aiohttp.txt

aiohttp.txt: aiohttp-clear
	echo "aiohttp==2.0.6.post1" > aiohttp.txt

aiohttp-clear:
	rm -f aiohttp
	rm -f aiohttp.txt
	rm -f aiohttp.nix
	rm -f aiohttp_frozen.txt


#------------------------------------------------------------------------------


awscli_and_requests: awscli_and_requests.nix
	echo "building and testing awscli and requests library ..."
	$(NIX_BUILD) awscli_and_requests.nix -o awscli_and_requests interpreter $(AFTER)
	./awscli_and_requests/bin/python -c 'import awscli; import requests'
	PAGER=none ./awscli_and_requests/bin/aws help
	$(NIX_SHELL) awscli_and_requests.nix interpreter --command python -c 'import awscli'
	$(NIX_SHELL) awscli_and_requests.nix interpreter --command python -c 'import awscli; import requests'
	PAGER=none $(NIX_SHELL) awscli_and_requests.nix interpreter --command aws help

awscli_and_requests.nix: awscli_and_requests.txt $(PYPI2NIX)
	echo "generating awscli and requests nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "2.7" \
    -e setuptools-scm \
		--basename awscli_and_requests \
		-r awscli_and_requests.txt

awscli_and_requests.txt: awscli_and_requests-clear
	echo "awscli" > awscli_and_requests.txt
	echo "requests" >> awscli_and_requests.txt

awscli_and_requests-clear:
	rm -f awscli_and_requests
	rm -f awscli_and_requests.txt
	rm -f awscli_and_requests.nix
	rm -f awscli_and_requests_frozen.txt


#------------------------------------------------------------------------------


connexion: connexion.nix
	echo "building and testing connexion..."
	$(NIX_BUILD) connexion.nix -o connexion interpreter $(AFTER)
	./connexion/bin/python -c 'import connexion'
	$(NIX_SHELL) connexion.nix interpreter --command python -c 'import connexion'

connexion.nix: connexion.txt $(PYPI2NIX)
	echo "generating connexion.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V 3.7 \
		-e pytest-runner \
		-e setuptools-scm \
		-e flake8 \
		--basename connexion \
		-r connexion.txt  \
		-e vcversioner

connexion.txt: connexion-clear
	echo "connexion" > connexion.txt

connexion-clear:
	rm -f connexion
	rm -f connexion.txt
	rm -f connexion.nix
	rm -f connexion_frozen.txt


#------------------------------------------------------------------------------


empy: empy.nix
	echo "building and testing empy ..."
	$(NIX_BUILD) empy.nix -o empy interpreter $(AFTER)
	./empy/bin/python -c 'import em'
	$(NIX_SHELL) empy.nix interpreter --command python -c 'import em'

empy.nix: empy.txt $(PYPI2NIX)
	echo "generating empy nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "2.7" \
		--basename empy \
		-r empy.txt

empy.txt: empy-clear
	echo "empy" > empy.txt

empy-clear:
	rm -f empy
	rm -f empy.txt
	rm -f empy.nix
	rm -f empy_frozen.txt


#------------------------------------------------------------------------------


flake8: flake8.nix
	echo "building and testing flake8..."
	$(NIX_BUILD) flake8.nix -o flake8 interpreter $(AFTER)
	./flake8/bin/python -c 'import flake8'
	$(NIX_SHELL) flake8.nix interpreter --command python -c 'import flake8'

flake8.nix: flake8.txt $(PYPI2NIX)
	echo "generating flake8.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.5" \
    -e pytest-runner \
    -e setuptools-scm \
		--basename flake8 \
		-r flake8.txt

flake8.txt: flake8-clear
	echo "flake8" > flake8.txt

flake8-clear:
	rm -f flake8
	rm -f flake8.txt
	rm -f flake8.nix
	rm -f flake8_frozen.txt


#------------------------------------------------------------------------------


ldap: ldap.nix
	echo "building and testing ldap..."
	$(NIX_BUILD) ldap.nix -o ldap interpreter $(AFTER)
	./ldap/bin/python -c 'import ldap'
	$(NIX_SHELL) ldap.nix interpreter --command python -c 'import ldap'

ldap.nix: ldap.txt $(PYPI2NIX)
	echo "generating ldap.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "2.7" \
		--basename ldap \
		-N "NIX_CFLAGS_COMPILE=\"-I\$${pkgs.cyrus_sasl.dev}/include/sasl \$$NIX_CFLAGS_COMPILE\"" \
		-E "openldap cyrus_sasl openssl" \
		-r ldap.txt

ldap.txt: ldap-clear
	echo "python-ldap" > ldap.txt

ldap-clear:
	rm -f ldap
	rm -f ldap.txt
	rm -f ldap.nix
	rm -f ldap_frozen.txt


#------------------------------------------------------------------------------


lektor: lektor.nix
	echo "building and testing lektor ..."
	$(NIX_BUILD) lektor.nix -o lektor interpreter $(AFTER)
	./lektor/bin/python -c 'import lektor'
	./lektor/bin/lektor --help
	$(NIX_SHELL) lektor.nix interpreter --command python -c 'import lektor'
	$(NIX_SHELL) lektor.nix interpreter --command lektor --help

lektor.nix: lektor.txt $(PYPI2NIX)
	echo "generating lektor nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "2.7" \
		--basename lektor \
		-E $(LEKTOR_BUILD_INPUTS) \
		-r lektor.txt

lektor.txt: lektor-clear
	echo "Lektor" > lektor.txt

lektor-clear:
	rm -f lektor
	rm -f lektor.txt
	rm -f lektor.nix
	rm -f lektor_frozen.txt


#------------------------------------------------------------------------------


mercurial: mercurial.nix
	echo "building and testing mercurial..."
	$(NIX_BUILD) mercurial.nix -o mercurial interpreter $(AFTER)
	./mercurial/bin/python -c 'import flake8'
	$(NIX_SHELL) mercurial.nix interpreter --command python -c 'import flake8'
	if ./string_in_file "a209fb6" mercurial.nix ; then true ; else echo "ERROR: Revision 'a209fb6' not found in tornado.nix!"; exit 123; fi

mercurial.nix: mercurial.txt $(PYPI2NIX)
	echo "generating mercurial.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "2.7" \
		-e pytest-runner \
		-e setuptools-scm \
		--basename mercurial \
		-E "mercurial" \
		-r mercurial.txt


mercurial.txt: mercurial-clear
	echo "-e hg+https://bitbucket.org/tarek/flake8@a209fb6#egg=flake8" > mercurial.txt

mercurial-clear:
	rm -f mercurial
	rm -f mercurial.txt
	rm -f mercurial.nix
	rm -f mercurial_frozen.txt


#------------------------------------------------------------------------------


pillow: pillow.nix
	echo "building and testing pillow..."
	$(NIX_BUILD) pillow.nix -o pillow interpreter $(AFTER)
	./pillow/bin/python -c 'import PIL'
	$(NIX_SHELL) pillow.nix interpreter --command python -c 'import PIL'

pillow.nix: pillow.txt $(PYPI2NIX)
	echo "generating pillownix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.5" \
		--basename pillow \
		-E "pkgconfig zlib libjpeg openjpeg libtiff freetype lcms2 libwebp tcl" \
		-r pillow.txt

pillow.txt: pillow-clear
	echo "Pillow" > pillow.txt

pillow-clear:
	rm -f pillow
	rm -f pillow.txt
	rm -f pillow.nix
	rm -f pillow_frozen.txt


#------------------------------------------------------------------------------


rss2email: rss2email.nix
	echo "building and testing rss2email ..."
	$(NIX_BUILD) rss2email.nix -o rss2email interpreter $(AFTER)
	./rss2email/bin/python -c 'import rss2email'
	./rss2email/bin/r2e --help
	$(NIX_SHELL) rss2email.nix interpreter --command python -c 'import rss2email'
	$(NIX_SHELL) rss2email.nix interpreter --command r2e --help

rss2email.nix: rss2email.txt $(PYPI2NIX)
	echo "generating rss2email nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.6" \
		--basename rss2email \
		-r rss2email.txt

rss2email.txt: rss2email-clear
	echo "https://github.com/wking/rss2email/archive/master.zip#egg=rss2email" > rss2email.txt

rss2email-clear:
	rm -f rss2email
	rm -f rss2email.txt
	rm -f rss2email.nix
	rm -f rss2email_frozen.txt


#------------------------------------------------------------------------------


scipy: scipy.nix
	echo "building and testing scipy..."
	$(NIX_BUILD) scipy.nix -o scipy interpreter $(AFTER)
	./scipy/bin/python -c 'import scipy'
	$(NIX_SHELL) scipy.nix interpreter --command python -c 'import scipy'

scipy.nix: scipy.txt $(PYPI2NIX)
	echo "generating scipy.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.5" \
		--basename scipy \
		-s numpy \
		-E gfortran \
		-E blas \
		-r scipy.txt

scipy.txt: scipy-clear
	echo "scipy" > scipy.txt
	echo "numpy" >> scipy.txt

scipy-clear:
	rm -f scipy
	rm -f scipy.txt
	rm -f scipy.nix
	rm -f scipy_frozen.txt


#------------------------------------------------------------------------------


tornado: tornado.nix
	echo "building and testing tornado..."
	$(NIX_BUILD) tornado.nix -o tornado interpreter $(AFTER)
	./tornado/bin/python -c 'import tornado'
	$(NIX_SHELL) tornado.nix interpreter --command python -c 'import tornado'
	if ./string_in_file "69253c820df473407c562a227d0ba36df25018ab" tornado.nix ; then true ; else echo "ERROR: Revision '69253c820df473407c562a227d0ba36df25018ab' not found in tornado.nix!" ; exit 123 ; fi

tornado.nix: tornado.txt $(PYPI2NIX)
	echo "generating tornado.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.5" \
		--basename tornado \
		-r tornado.txt

tornado.txt: tornado-clear
	echo "-e git+git://github.com/tornadoweb/tornado.git@69253c820df473407c562a227d0ba36df25018ab#egg=tornado" > tornado.txt

tornado-clear:
	rm -f tornado
	rm -f tornado.txt
	rm -f tornado.nix
	rm -f tornado_frozen.txt


#------------------------------------------------------------------------------


packages_with: packages_with.nix
	echo "building and testing packages_with..."
	$(NIX_BUILD) packages_with.nix -o packages_with interpreter $(AFTER)
	sh test_with_packages.sh

packages_with.nix: packages_with.txt $(PYPI2NIX)
	echo "generating packages_with.nix expressions ..."
	$(PYPI2NIX) -v \
		-I $(NIX_PATH) \
		-V "3.6" \
		--basename packages_with \
		-r packages_with.txt

packages_with.txt: packages_with-clear
	echo "tornado" > packages_with.txt
	echo "flake8" >> packages_with.txt

packages_with-clear:
	rm -f packages_with
	rm -f packages_with.txt
	rm -f packages_with.nix
	rm -f packages_with_frozen.txt
