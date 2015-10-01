{ stdenv
, fetchurl
, unzip
, which
, makeWrapper
, python
, pipWhlVersion ? "7.1.2"
, pipWhlHash ? "5ff9fec0be479e4e36df467556deed4d"
, setuptoolsWhlVersion ?  "18.3.2"
, setuptoolsWhlHash ? "58c1e15fe0c124ab0880a2691f232434"
, pipVersion ?  "7.1.2"
, pipHash ? "3823d2343d9f3aaab21cf9c917710196"
, buildoutVersion ? "2.4.3"
, buildoutHash ? "32dcb3de0673193b78d670c29551ef6c"
, buildoutReqsVersion ? "0.2.2"
, buildoutReqsHash ? "78104e62a71d9a8d315648a4b2574e76"
, wheelVersion ? "0.26.0"
, wheelHash ? "4cfc6e7e3dc7377d0164914623922a10"
}:

let
  pypiurl = "https://pypi.python.org/packages/source";
  pipWhl = fetchurl { url = "https://pypi.python.org/packages/py2.py3/p/pip/pip-${pipWhlVersion}-py2.py3-none-any.whl"; md5 = pipWhlHash; };
  setuptoolsWhl = fetchurl { url = "https://pypi.python.org/packages/3.4/s/setuptools/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl"; md5 = setuptoolsWhlHash; };
  pip = fetchurl { url = "${pypiurl}/p/pip/pip-${pipVersion}.tar.gz"; md5 = pipHash; };
  buildout = fetchurl { url = "${pypiurl}/z/zc.buildout/zc.buildout-${buildoutVersion}.tar.gz"; md5 = buildoutHash; };
  buildoutReqs = fetchurl { url = "${pypiurl}/b/buildout.requirements/buildout.requirements-${buildoutReqsVersion}.tar.gz"; md5 = buildoutReqsHash; };
  wheel = fetchurl { url = "${pypiurl}/w/wheel/wheel-${wheelVersion}.tar.gz"; md5 = wheelHash; };
in
  stdenv.mkDerivation {
    name = "pypi2nix-bootstrap";
    src = pip;
    buildInputs = [ which python makeWrapper ];
    installPhase = ''
      mkdir -p $out/bin $out/site-packages

      mkdir index/
      cp ${pipWhl} index/pip-${pipWhlVersion}-py2.py3-none-any.whl
      cp ${setuptoolsWhl} index/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl
      cp ${wheel} index/wheel-${wheelVersion}.tar.gz
      cp ${buildout} index/zc.buildout-${buildoutVersion}.tar.gz
      cp ${buildoutReqs} index/buildout.requirements-${buildoutReqsVersion}.tar.gz

      mkdir tmp
      mv pip tmp/
      cd tmp

      python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'pip', 'setuptools', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/base']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'wheel', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/extra']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'zc.buildout', 'buildout.requirements', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/extra']))"
      touch $out/extra/zc/__init__.py
      touch $out/extra/buildout/__init__.py

      echo -e "#!${python}/bin/python\nimport sys, pip; sys.exit(pip.main())" > $out/bin/pip
      echo -e "#!${python}/bin/python\nimport sys, zc.buildout.buildout\nsys.exit(zc.buildout.buildout.main())" > $out/bin/buildout

      chmod +x $out/bin/*
    '';
  }
