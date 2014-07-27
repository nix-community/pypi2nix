DESTDIR=$(shell realpath build)

all:

$(DESTDIR)/: $(DESTDIR)/bin/pypi2nix

$(DESTDIR)/bin/pypi2nix: src/
	mkdir $(DESTDIR)/bin
	cd $< && zip -qr pypi2nix.zip * && cd ..
	echo '#!/usr/bin/env python' | cat - $<pypi2nix.zip > $(DESTDIR)/bin/pypi2nix
	chmod +x $(DESTDIR)/bin/pypi2nix
	rm $<pypi2nix.zip

install: $(DESTDIR)/

.PHONY: all install
