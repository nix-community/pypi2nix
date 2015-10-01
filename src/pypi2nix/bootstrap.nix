{ stdenv
, fetchurl
, unzip
, which
, makeWrapper
, python
, pipVersion ?  "6.0.8"
, pipHash ? "2332e6f97e75ded3bddde0ced01dbda3"
, pipWhlVersion ? "6.0.8"
, pipWhlHash ? "41e73fae2c86ba2270ff51c1d86f7e09"
, setuptoolsWhlVersion ?  "15.0"
, setuptoolsWhlHash ? "80570f4e94f9c05a35241a53c38d3540"
, buildoutVersion ? "2.3.1"
, buildoutHash ? "cbf008369ca28814ed8051084622fba8"
, buildoutDumpReqVersion ? "0.1.1"
, buildoutDumpReqHash ? "b4133d469743e8280a761d616c146983"
, wheelVersion ? "0.24.0"
, wheelHash ? "3b0d66f0d127ea8befaa5d11453107fd"
}:

let
  pypiurl = "https://pypi.python.org/packages/source";
  pipWhl = fetchurl { url = "https://pypi.python.org/packages/py2.py3/p/pip/pip-${pipWhlVersion}-py2.py3-none-any.whl"; md5 = pipWhlHash; };
  setuptoolsWhl = fetchurl { url = "https://pypi.python.org/packages/3.4/s/setuptools/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl"; md5 = setuptoolsWhlHash; };
  pip = fetchurl { url = "${pypiurl}/p/pip/pip-${pipVersion}.tar.gz"; md5 = pipHash; };
  buildout = fetchurl { url = "${pypiurl}/z/zc.buildout/zc.buildout-${buildoutVersion}.tar.gz"; md5 = buildoutHash; };
  buildoutDumpReq = fetchurl { url = "${pypiurl}/b/buildout.dumprequirements/buildout.dumprequirements-${buildoutDumpReqVersion}.tar.gz"; md5 = buildoutDumpReqHash; };
  wheel = fetchurl { url = "${pypiurl}/w/wheel/wheel-${wheelVersion}.tar.gz"; md5 = wheelHash; };
in
  stdenv.mkDerivation {
    name = "pypi2nix-bootstrap";
    src = pip;
    buildInputs = [ which python makeWrapper ];
    installPhase = ''
      mkdir -p $out/bin $out/base $out/extra

      mkdir index/
      cp ${pipWhl} index/pip-${pipWhlVersion}-py2.py3-none-any.whl
      cp ${setuptoolsWhl} index/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl
      cp ${wheel} index/wheel-${wheelVersion}.tar.gz
      cp ${buildout} index/zc.buildout-${buildoutVersion}.tar.gz
      cp ${buildoutDumpReq} index/buildout.dumprequirements-${buildoutDumpReqVersion}.tar.gz

      mkdir tmp
      mv pip tmp/
      cd tmp

      python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'pip', 'setuptools', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/base']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'wheel', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/base']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'zc.buildout', 'buildout.dumprequirements', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/extra']))"
      touch $out/extra/zc/__init__.py
      touch $out/extra/buildout/__init__.py

      echo -e "#!${python}/bin/python\nimport sys, pip; sys.exit(pip.main())" > $out/bin/pip
      echo -e "#!${python}/bin/python\nimport sys, zc.buildout.buildout\nsys.exit(zc.buildout.buildout.main())" > $out/bin/buildout
      for prog in $out/bin/*; do
        chmod +x "$prog"
        wrapProgram "$prog" --set PYTHONPATH "$out/base:$out/extra"
      done
    '';
  }
