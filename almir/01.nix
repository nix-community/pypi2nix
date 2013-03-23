{ pkgs, python, pythonPackages, buildPythonPackage }:

let almir014Packages = python.modules // rec {
  inherit python;
  inherit (pythonPackages) setuptools;
  inherit (pkgs) fetchurl stdenv;

  pyramid = buildPythonPackage rec {
    name = "pyramid-1.3.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pyramid/pyramid-1.3.4.tar.gz";
      md5 = "967a04fcb2143b31b279c3013a778a2b";
    };
    buildInputs = [ virtualenv venusian sphinx zope_component translationstring repoze_lru mako pastedeploy repoze_sphinx_autointerface docutils webob zope_interface setuptools webtest chameleon zope_deprecation ];
    propagatedBuildInputs = [ venusian translationstring repoze_lru mako pastedeploy webob zope_interface setuptools chameleon zope_deprecation ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  routes = buildPythonPackage rec {
    name = "Routes-1.13";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/R/Routes/Routes-1.13.tar.gz";
      md5 = "d527b0ab7dd9172b1275a41f97448783";
    };
    buildInputs = [ repoze_lru paste nose webtest ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pyramid_exclog = buildPythonPackage rec {
    name = "pyramid_exclog-0.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pyramid_exclog/pyramid_exclog-0.6.tar.gz";
      md5 = "5c18706f5500605416afff311120c933";
    };
    buildInputs = [ pyramid ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  almir = buildPythonPackage rec {
    name = "almir-0.1.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/a/almir/almir-0.1.4.tar.gz";
      md5 = "be43a6dc7c667b9ad5a243e0e76d8917";
    };
    buildInputs = [ pkgs.makeWrapper pyramid zope_sqlalchemy pyramid_exclog tissue deform webhelpers mysql_connector_repackaged webtest pyramid_jinja2 docutils deform_bootstrap pg8000 unittest2 mock pyramid_tm sqlalchemy pytz coverage transaction pyramid_beaker colander nose waitress ];
    propagatedBuildInputs = [ pyramid_tm pyramid zope_sqlalchemy pyramid_exclog pytz webhelpers mysql_connector_repackaged pyramid_beaker colander docutils transaction deform_bootstrap pg8000 sqlalchemy pyramid_jinja2 waitress deform pkgs.python27Full pythonPackages.recursivePthLoader ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    postInstall = ''
      ln -s ${pyramid}/bin/pserve $out/bin
      wrapProgram "$out/bin/pserve" \
        --suffix PYTHONPATH : "$out/lib/python2.7/site-packages"
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zeo = buildPythonPackage rec {
    name = "ZEO-4.0.0a1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZEO/ZEO-4.0.0a1.tar.gz";
      md5 = "63d983f65625ea0ec87167e4b1868d0f";
    };
    buildInputs = [ zope_testing transaction zdaemon persistent zconfig zodb zope_interface manuel zc_lockfile ];
    propagatedBuildInputs = [ zdaemon zconfig zodb zc_lockfile ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zconfig = buildPythonPackage rec {
    name = "ZConfig-3.0.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZConfig/ZConfig-3.0.3.tar.gz";
      md5 = "60a107c5857c3877368dfe5930559804";
    };
    buildInputs = [ zope_testrunner ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_sqlalchemy = buildPythonPackage rec {
    name = "zope.sqlalchemy-0.7.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.sqlalchemy/zope.sqlalchemy-0.7.2.zip";
      md5 = "b654e5d144ed141e13b42591a21a4868";
    };
    buildInputs = [ pkgs.unzip sqlalchemy transaction zope_testing zope_interface setuptools ];
    propagatedBuildInputs = [ sqlalchemy ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pygments = buildPythonPackage rec {
    name = "Pygments-1.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Pygments/Pygments-1.4.tar.gz";
      md5 = "d77ac8c93a7fb27545f2522abe9cc462";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zodb = buildPythonPackage rec {
    name = "ZODB-4.0.0a4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZODB/ZODB-4.0.0a4.tar.gz";
      md5 = "c6418f599f499d257da1c281c8f219d1";
    };
    buildInputs = [ persistent zope_testing transaction zdaemon persistent zconfig zope_interface manuel btrees zc_lockfile ];
    propagatedBuildInputs = [ zc_lockfile ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  sqlalchemy = buildPythonPackage rec {
    name = "SQLAlchemy-0.7.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-0.7.6.tar.gz";
      md5 = "6383cade61ecff1a236708fae066447a";
    };
    buildInputs = [ nose ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pyramid_jinja2 = buildPythonPackage rec {
    name = "pyramid_jinja2-1.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pyramid_jinja2/pyramid_jinja2-1.6.zip";
      md5 = "b7df1ab97f90f39529d27ba6da1f6b1c";
    };
    buildInputs = [ pkgs.unzip jinja2 pyramid webtest ];
    propagatedBuildInputs = [ jinja2 ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  beautifulsoup4 = buildPythonPackage rec {
    name = "beautifulsoup4-4.1.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-4.1.3.tar.gz";
      md5 = "c012adc06217b8532c446d181cc56586";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  deform = buildPythonPackage rec {
    name = "deform-0.9.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/deform/deform-0.9.4.tar.gz";
      md5 = "2ed7b69644a6d8f4e1404e1892329240";
    };
    buildInputs = [ beautifulsoup4 peppercorn colander translationstring chameleon ];
    propagatedBuildInputs = [ peppercorn colander ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  virtualenv = buildPythonPackage rec {
    name = "virtualenv-1.9.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz";
      md5 = "07e09df0adfca0b2d487e39a4bf2270a";
    };
    buildInputs = [ nose mock ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_testing = buildPythonPackage rec {
    name = "zope.testing-4.1.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.testing/zope.testing-4.1.2.zip";
      md5 = "01c30c342c6a18002a762bd5d320a6e9";
    };
    buildInputs = [ pkgs.unzip zope_interface zope_exceptions setuptools ];
    propagatedBuildInputs = [ zope_interface zope_exceptions setuptools ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  repoze_lru = buildPythonPackage rec {
    name = "repoze.lru-0.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/r/repoze.lru/repoze.lru-0.4.tar.gz";
      md5 = "9f6ab7a4ff871ba795cadf56c20fb0f0";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pep8 = buildPythonPackage rec {
    name = "pep8-1.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pep8/pep8-1.2.tar.gz";
      md5 = "057cf01c3099d795da5f9a193410ab2f";
    };
    buildInputs = [ setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  repoze_sphinx_autointerface = buildPythonPackage rec {
    name = "repoze.sphinx.autointerface-0.7.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/r/repoze.sphinx.autointerface/repoze.sphinx.autointerface-0.7.1.tar.gz";
      md5 = "f2fee996ae28dc16eb48f1a3e8f64801";
    };
    buildInputs = [ zope_interface setuptools sphinx ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  six = buildPythonPackage rec {
    name = "six-1.3.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/s/six/six-1.3.0.tar.gz";
      md5 = "ec47fe6070a8a64c802363d2c2b1e2ee";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  webtest = buildPythonPackage rec {
    name = "WebTest-1.3.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/W/WebTest/WebTest-1.3.3.zip";
      md5 = "51ce57701ad81f8962b2876926b20772";
    };
    buildInputs = [ pkgs.unzip webob nose dtopt ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_exceptions = buildPythonPackage rec {
    name = "zope.exceptions-4.0.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.exceptions/zope.exceptions-4.0.6.zip";
      md5 = "63cf38f8081e9e3b73eaf8725ba8dda6";
    };
    buildInputs = [ pkgs.unzip zope_interface setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  btrees = buildPythonPackage rec {
    name = "BTrees-4.0.5";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/B/BTrees/BTrees-4.0.5.tar.gz";
      md5 = "bdba5ef674bfea95f8a80eafed1acc13";
    };
    buildInputs = [ persistent zope_interface ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  docutils = buildPythonPackage rec {
    name = "docutils-0.9.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/docutils/docutils-0.9.1.tar.gz";
      md5 = "b0d5cd5298fedf9c62f5fd364a274d56";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zodb3 = buildPythonPackage rec {
    name = "ZODB3-3.11.0a3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZODB3/ZODB3-3.11.0a3.tar.gz";
      md5 = "ce34ed7452fb972344ef2bf3152775d9";
    };
    buildInputs = [ transaction btrees zeo persistent zeo btrees zodb zodb persistent ];
    propagatedBuildInputs = [ btrees transaction zodb persistent zeo ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pytz = buildPythonPackage rec {
    name = "pytz-2013b";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pytz/pytz-2013b.zip";
      md5 = "c70dc37ffe435dd77e3f967a0dffe928";
    };
    buildInputs = [ pkgs.unzip ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pastedeploy = buildPythonPackage rec {
    name = "PasteDeploy-1.5.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/PasteDeploy/PasteDeploy-1.5.0.tar.gz";
      md5 = "f1a068a0b680493b6eaff3dd7690690f";
    };
    buildInputs = [ nose ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  deform_bootstrap = buildPythonPackage rec {
    name = "deform_bootstrap-0.2.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/deform_bootstrap/deform_bootstrap-0.2.6.tar.gz";
      md5 = "10aa4f5fd37a126506dc179805e6b061";
    };
    buildInputs = [ deform ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_testrunner = buildPythonPackage rec {
    name = "zope.testrunner-4.3.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.testrunner/zope.testrunner-4.3.3.zip";
      md5 = "741bfa4d63db4a3ce27908889a8826a3";
    };
    buildInputs = [ pkgs.unzip zope_exceptions six setuptools zope_interface ];
    propagatedBuildInputs = [ six ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  webob = buildPythonPackage rec {
    name = "WebOb-1.2b3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/W/WebOb/WebOb-1.2b3.zip";
      md5 = "e0cdf8657fd77b1da7c12bed838596ba";
    };
    buildInputs = [ pkgs.unzip nose ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  unittest2 = buildPythonPackage rec {
    name = "unittest2-0.5.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/u/unittest2/unittest2-0.5.1.zip";
      md5 = "1527fb89e38343945af1166342d851ee";
    };
    buildInputs = [ pkgs.unzip ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  mock = buildPythonPackage rec {
    name = "mock-1.0.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/m/mock/mock-1.0.1.zip";
      md5 = "869f08d003c289a97c1a6610faf5e913";
    };
    buildInputs = [ pkgs.unzip unittest2 ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pyramid_tm = buildPythonPackage rec {
    name = "pyramid_tm-0.7";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pyramid_tm/pyramid_tm-0.7.tar.gz";
      md5 = "6dc917d262c69366630c542bd21859a3";
    };
    buildInputs = [ transaction pyramid ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  mako = buildPythonPackage rec {
    name = "Mako-0.6.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/M/Mako/Mako-0.6.2.tar.gz";
      md5 = "b467eb01c2227e205784faa3bef96725";
    };
    buildInputs = [ markupsafe nose ];
    propagatedBuildInputs = [ markupsafe ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_deprecation = buildPythonPackage rec {
    name = "zope.deprecation-3.5.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.deprecation/zope.deprecation-3.5.0.tar.gz";
      md5 = "1e7db82583013127aab3e7e790b1f2b6";
    };
    buildInputs = [ zope_testing setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  dtopt = buildPythonPackage rec {
    name = "dtopt-0.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/dtopt/dtopt-0.1.tar.gz";
      md5 = "9a41317149e926fcc408086aedee6bab";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  mysql_connector_repackaged = buildPythonPackage rec {
    name = "mysql-connector-repackaged-0.3.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/m/mysql-connector-repackaged/mysql-connector-repackaged-0.3.1.tar.gz";
      md5 = "0b17ad1cb3fe763fd44487cb97cf45b2";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zc_lockfile = buildPythonPackage rec {
    name = "zc.lockfile-1.1.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zc.lockfile/zc.lockfile-1.1.0.zip";
      md5 = "8e46b830417363501363bd09e1af1ecc";
    };
    buildInputs = [ pkgs.unzip zope_testing setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  markupsafe = buildPythonPackage rec {
    name = "MarkupSafe-0.15";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-0.15.tar.gz";
      md5 = "4e7c4d965fe5e033fa2d7bb7746bb186";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_hookable = buildPythonPackage rec {
    name = "zope.hookable-4.0.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.hookable/zope.hookable-4.0.1.tar.gz";
      md5 = "5a97fcf312586ee90d4cb83b7206e609";
    };
    buildInputs = [ zope_testing setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  jinja2 = buildPythonPackage rec {
    name = "Jinja2-2.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.6.tar.gz";
      md5 = "1c49a8825c993bfdcf55bb36897d28a2";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  coverage = buildPythonPackage rec {
    name = "coverage-3.5.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/c/coverage/coverage-3.5.1.tar.gz";
      md5 = "410d4c8155a4dab222f2bc51212d4a24";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pg8000 = buildPythonPackage rec {
    name = "pg8000-1.05";
    src = fetchurl {
      url = "http://pybrary.net/pg8000/dist/pg8000-1.08.tar.gz";
      md5 = "2e8317a22d0e09a6f12e98ddf3bb75fd";
    };
    buildInputs = [ pkgs.unzip pytz ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  peppercorn = buildPythonPackage rec {
    name = "peppercorn-0.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/peppercorn/peppercorn-0.4.tar.gz";
      md5 = "464d6f2342eaf704dfb52046c1f5c320";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  chameleon = buildPythonPackage rec {
    name = "Chameleon-2.7.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/C/Chameleon/Chameleon-2.7.3.tar.gz";
      md5 = "c40243b8b68081ad6733673c02b65369";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  translationstring = buildPythonPackage rec {
    name = "translationstring-0.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/t/translationstring/translationstring-0.4.tar.gz";
      md5 = "392287923c475b660b7549b2c2f03dbc";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  paste = buildPythonPackage rec {
    name = "Paste-1.7.5.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Paste/Paste-1.7.5.1.tar.gz";
      md5 = "7ea5fabed7dca48eb46dc613c4b6c4ed";
    };
    buildInputs = [ nose ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  beaker = buildPythonPackage rec {
    name = "Beaker-1.6.4";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/B/Beaker/Beaker-1.6.4.tar.gz";
      md5 = "c2e102870ed4c53104dec48ceadf8e9d";
    };
    buildInputs = [ sqlalchemy pycryptopp nose mock webtest ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  transaction = buildPythonPackage rec {
    name = "transaction-1.1.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/t/transaction/transaction-1.1.1.tar.gz";
      md5 = "30b062baa34fe1521ad979fb088c8c55";
    };
    buildInputs = [ zope_interface ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  sphinx = buildPythonPackage rec {
    name = "Sphinx-1.1.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/S/Sphinx/Sphinx-1.1.2.tar.gz";
      md5 = "b65a5d5d6172f3dcfefb4770ec63926e";
    };
    buildInputs = [ jinja2 docutils pygments ];
    propagatedBuildInputs = [ jinja2 docutils pygments ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zdaemon = buildPythonPackage rec {
    name = "zdaemon-4.0.0a1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zdaemon/zdaemon-4.0.0a1.zip";
      md5 = "56799a919bc073bce5289b773ee64595";
    };
    buildInputs = [ pkgs.unzip ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_component = buildPythonPackage rec {
    name = "zope.component-3.12.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.component/zope.component-3.12.0.tar.gz";
      md5 = "1002e3be68c56751335c185f01b286fb";
    };
    buildInputs = [ zope_testing zope_hookable zodb3 zope_event zope_interface setuptools zope_testrunner ];
    propagatedBuildInputs = [ zope_event zope_interface setuptools ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  webhelpers = buildPythonPackage rec {
    name = "WebHelpers-1.3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/W/WebHelpers/WebHelpers-1.3.tar.gz";
      md5 = "32749ffadfc40fea51075a7def32588b";
    };
    buildInputs = [ routes markupsafe webob nose ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  tissue = buildPythonPackage rec {
    name = "tissue-0.7";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/t/tissue/tissue-0.7.tar.gz";
      md5 = "c9f3772407eb7499a949daaa9b859fdf";
    };
    buildInputs = [ pep8 nose ];
    propagatedBuildInputs = [ pep8 ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  persistent = buildPythonPackage rec {
    name = "persistent-4.0.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/persistent/persistent-4.0.6.tar.gz";
      md5 = "556dcac67448bf00111bae7e30fcec87";
    };
    buildInputs = [ zope_interface ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pyramid_beaker = buildPythonPackage rec {
    name = "pyramid_beaker-0.7";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pyramid_beaker/pyramid_beaker-0.7.tar.gz";
      md5 = "acb863517a98b90b5f29648ce55dd563";
    };
    buildInputs = [ beaker pyramid ];
    propagatedBuildInputs = [ beaker ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  colander = buildPythonPackage rec {
    name = "colander-0.9.6";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/c/colander/colander-0.9.6.tar.gz";
      md5 = "2d9f65a64cb6b7f35d6a0d7b607ce4c6";
    };
    buildInputs = [ translationstring ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  venusian = buildPythonPackage rec {
    name = "venusian-1.0a3";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/v/venusian/venusian-1.0a3.tar.gz";
      md5 = "7e3a522772ed2c98e9922ade569c7474";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_event = buildPythonPackage rec {
    name = "zope.event-3.5.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.event/zope.event-3.5.1.tar.gz";
      md5 = "f18363bf9926f1762fa580cc69bd97ec";
    };
    buildInputs = [ setuptools ];
    propagatedBuildInputs = [ setuptools ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  nose = buildPythonPackage rec {
    name = "nose-1.1.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/n/nose/nose-1.1.2.tar.gz";
      md5 = "144f237b615e23f21f6a50b2183aa817";
    };
    buildInputs = [  ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  manuel = buildPythonPackage rec {
    name = "manuel-1.7.2";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/m/manuel/manuel-1.7.2.tar.gz";
      md5 = "3c4d173072b5cc1c4ccf6739498b77b5";
    };
    buildInputs = [ zope_testing six setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  pycryptopp = buildPythonPackage rec {
    name = "pycryptopp-0.6.0.1206569328141510525648634803928199668821045408958";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pycryptopp/pycryptopp-0.6.0.1206569328141510525648634803928199668821045408958.tar.gz";
      md5 = "ce38fbe03705d27da408c78b56eb1947";
    };
    buildInputs = [ setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  zope_interface = buildPythonPackage rec {
    name = "zope.interface-3.8.0";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.interface/zope.interface-3.8.0.tar.gz";
      md5 = "8ab837320b4532774c9c89f030d2a389";
    };
    buildInputs = [ zope_event setuptools ];
    propagatedBuildInputs = [ setuptools ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

  waitress = buildPythonPackage rec {
    name = "waitress-0.8.1";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/w/waitress/waitress-0.8.1.tar.gz";
      md5 = "aadfc692b780fc42eb05ac819102d336";
    };
    buildInputs = [ setuptools ];
    propagatedBuildInputs = [  ];
    installCommand = ''
      easy_install --always-unzip --no-deps --prefix="$out" .
    '';
    doCheck = false;
    meta = {
       maintainers = [
         stdenv.lib.maintainers.garbas
         stdenv.lib.maintainers.iElectric
      ];
    };
  };

}; in almir014Packages
