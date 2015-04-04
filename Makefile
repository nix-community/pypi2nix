DESTDIR=$(shell realpath build)
CLICK_VERSION=2.5
CLICK_HASH=a1bff2d2270745affd5bc60e66e50c23
SETUPTOOLS_VERSION=5.5.1
SETUPTOOLS_HASH=86bbbfa732c234535316a7d74a49c6ad
ZC_BUILDOUT_VERSION=2.2.1
ZC_BUILDOUT_HASH=476a06eed08506925c700109119b6e41
ZC_RECIPE_EGG_VERSION=2.0.1
ZC_RECIPE_EGG_HASH=5e81e9d4cc6200f5b1abcf7c653dd9e3

all:

$(DESTDIR)/: $(DESTDIR)/pypi2nix

$(DESTDIR)/pypi2nix: src/
	@mkdir -p $(DESTDIR)
	@cd $< && zip -qr pypi2nix.zip * && cd ..
	@echo '#!/usr/bin/env python' | cat - $<pypi2nix.zip > $(DESTDIR)/pypi2nix
	@chmod +x $(DESTDIR)/pypi2nix
	@rm $<pypi2nix.zip
	@echo "$(DESTDIR)/pypi2nix" is ready to be used

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
	@if [ ! -f setuptools-$(SETUPTOOLS_VERSION).tar.gz ]; then \
		wget https://pypi.python.org/packages/source/s/setuptools/setuptools-$(SETUPTOOLS_VERSION).tar.gz;\
	fi
	@if [ `md5sum setuptools-${SETUPTOOLS_VERSION}.tar.gz | cut -b-32` != $(SETUPTOOLS_HASH) ]; then\
		rm setuptools-${SETUPTOOLS_VERSION}.tar.gz;\
		exit 1;\
	fi
	@tar zxf setuptools-${SETUPTOOLS_VERSION}.tar.gz
	@rm setuptools-${SETUPTOOLS_VERSION}.tar.gz
	@rm src/setuptools -rf
	@mv setuptools-${SETUPTOOLS_VERSION}/setuptools src/
	@rm setuptools-${SETUPTOOLS_VERSION} -rf
	@if [ ! -f zc.buildout-$(ZC_BUILDOUT_VERSION).tar.gz ]; then \
		wget https://pypi.python.org/packages/source/z/zc.buildout/zc.buildout-$(ZC_BUILDOUT_VERSION).tar.gz;\
	fi
	@if [ `md5sum zc.buildout-${ZC_BUILDOUT_VERSION}.tar.gz | cut -b-32` != $(ZC_BUILDOUT_HASH) ]; then\
		rm zc.buildout-${ZC_BUILDOUT_VERSION}.tar.gz;\
		exit 1;\
	fi
	@tar zxf zc.buildout-${ZC_BUILDOUT_VERSION}.tar.gz
	@rm zc.buildout-${ZC_BUILDOUT_VERSION}.tar.gz
	@rm src/zc -rf
	@mv zc.buildout-${ZC_BUILDOUT_VERSION}/src/zc src/
	@rm zc.buildout-${ZC_BUILDOUT_VERSION} -rf
	@if [ ! -f zc.recipe.egg-$(ZC_RECIPE_EGG_VERSION).tar.gz ]; then \
		wget https://pypi.python.org/packages/source/z/zc.recipe.egg/zc.recipe.egg-$(ZC_RECIPE_EGG_VERSION).tar.gz;\
	fi
	@if [ `md5sum zc.recipe.egg-${ZC_RECIPE_EGG_VERSION}.tar.gz | cut -b-32` != $(ZC_RECIPE_EGG_HASH) ]; then\
		rm zc.recipe.egg-${ZC_RECIPE_EGG_VERSION}.tar.gz;\
		exit 1;\
	fi
	@tar zxf zc.recipe.egg-${ZC_RECIPE_EGG_VERSION}.tar.gz
	@rm zc.recipe.egg-${ZC_RECIPE_EGG_VERSION}.tar.gz
	@rm src/zc/recipe -rf
	@mv zc.recipe.egg-${ZC_RECIPE_EGG_VERSION}/src/zc/recipe src/zc
	@rm zc.recipe.egg-${ZC_RECIPE_EGG_VERSION} -rf

clear:
	@rm -rf $(DESTDIR)

.PHONY: all install bootstrap
