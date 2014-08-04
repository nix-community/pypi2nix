DESTDIR=$(shell realpath build)
PIP_VERSION=1.5.6
PIP_HASH=01026f87978932060cc86c1dc527903e
CLICK_VERSION=2.5
CLICK_HASH=a1bff2d2270745affd5bc60e66e50c23

all:

$(DESTDIR)/: $(DESTDIR)/bin/pypi2nix

$(DESTDIR)/bin/pypi2nix: src/
	mkdir $(DESTDIR)/bin
	cd $< && zip -qr pypi2nix.zip * && cd ..
	echo '#!/usr/bin/env python' | cat - $<pypi2nix.zip > $(DESTDIR)/bin/pypi2nix
	chmod +x $(DESTDIR)/bin/pypi2nix
	rm $<pypi2nix.zip

install: $(DESTDIR)/

bootstrap:
	@if [ ! -f pip-$(PIP_VERSION).tar.gz ]; then \
		wget https://pypi.python.org/packages/source/p/pip/pip-$(PIP_VERSION).tar.gz;\
	fi
	@if [ `md5sum pip-${PIP_VERSION}.tar.gz | cut -b-32` != $(PIP_HASH) ]; then\
		rm pip-${PIP_VERSION}.tar.gz;\
		exit 1;\
	fi
	@tar zxf pip-${PIP_VERSION}.tar.gz
	@rm pip-${PIP_VERSION}.tar.gz
	@rm src/pip -rf
	@mv pip-${PIP_VERSION}/pip src/ 
	@rm pip-${PIP_VERSION} -rf
	@if [ ! -f click-$(CLICK_VERSION).tar.gz ]; then \
		wget https://pypi.python.org/packages/source/c/click/click-$(CLICK_VERSION).tar.gz;\
	fi
	@if [ `md5sum click-${CLICK_VERSION}.tar.gz | cut -b-32` != $(CLICK_HASH) ]; then\
		rm click-${CLICK_VERSION}.tar.gz;\
		exit 1;\
	fi
	@tar zxf click-${CLICK_VERSION}.tar.gz
	@rm click-${CLICK_VERSION}.tar.gz
	@rm src/click -rf
	@mv click-${CLICK_VERSION}/click src/ 
	@rm click-${CLICK_VERSION} -rf

.PHONY: all install bootstrap
