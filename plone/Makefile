
bootstrap: dev.nix
	nix-build --out-link nixenv dev.nix
	./nixenv/bin/virtualenv --distribute --clear .
	echo ../../../nixenv/lib/python2.7/site-packages > lib/python2.7/site-packages/nixenv.pth
	./bin/easy_install -H "" ipython
	./bin/easy_install -H "" ipdb
	./bin/easy_install -H "" zc.buildout


print-syspath:
	./bin/python -c 'import sys,pprint;pprint.pprint(sys.path)'


.PHONY: bootstrap print-syspath
