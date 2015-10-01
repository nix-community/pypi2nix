{ stdenv, fetchurl, unzip, which, makeWrapper, python }:

let

  pipVersion = "6.0.8";
  pipHash = "2332e6f97e75ded3bddde0ced01dbda3";
  setuptoolsWhlVersion ?  "15.0"
  setuptoolsWhlHash ? "80570f4e94f9c05a35241a53c38d3540"

  pip = fetchurl {
    url = "https://pypi.python.org/packages/py2.py3/p/pip/pip-${pipVersion}-py2.py3-none-any.whl";
    md5 = pipHash; };
  };

  setuptools = fetchurl {
    url = "https://pypi.python.org/packages/3.4/s/setuptools/setuptools-${setuptoolsVersion}-py2.py3-none-any.whl";
    md5 = setuptoolsHash;
 };
in 

  stdenv.mkDerivation {
    name = "${python.libPrefix}-pip-";
    src = pip;
    buildInputs = [ unzip which python makeWrapper ];
    unpackPhase = ''
      unzip $src -d tmp/
    '';
    installPhase = ''
      mkdir -p $out/bin
      ls -la

      mkdir index/
      cp ${pip} index/pip-${pipWhlVersion}-py2.py3-none-any.whl
      cp ${setuptools} index/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl
      cp ${wheel} index/wheel-${wheelVersion}.tar.gz
      cp ${buildout} index/zc.buildout-${buildoutVersion}.tar.gz
      cp ${buildoutDumpReq} index/buildout.dumprequirements-${buildoutDumpReqVersion}.tar.gz

      cd tmp

      python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'pip', 'setuptools', '--no-index', '--find-links=file://$PWD/../index', '--target', '$out']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'wheel', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/base']))"

      PYTHONPATH=$out/base python -c "import sys, pip; sys.exit(pip.main(['install', '--force-reinstall', '--upgrade', 'zc.buildout', 'buildout.dumprequirements', '--no-index', '--find-links=file://$PWD/../index', '-v', '--target', '$out/extra']))"

      printf "#!${pkgs.python}/bin/python\nimport sys, pip; sys.exit(pip.main())" > $out/bin/pip
      chmod +x $out/bin/pip
    '';
