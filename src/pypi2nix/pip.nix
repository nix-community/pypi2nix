{ path
, extraBuildInputs ? []
, cache ? null
, pipVersion ? "6.0.8"
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
  pkgs = import <nixpkgs> {};
  pypiurl = "https://pypi.python.org/packages/source";
  pipWhl = pkgs.fetchurl { url = "https://pypi.python.org/packages/py2.py3/p/pip/pip-${pipWhlVersion}-py2.py3-none-any.whl"; md5 = pipWhlHash; };
  setuptoolsWhl = pkgs.fetchurl { url = "https://pypi.python.org/packages/3.4/s/setuptools/setuptools-${setuptoolsWhlVersion}-py2.py3-none-any.whl"; md5 = setuptoolsWhlHash; };
  pip = pkgs.fetchurl { url = "${pypiurl}/p/pip/pip-${pipVersion}.tar.gz"; md5 = pipHash; };
  buildout = pkgs.fetchurl { url = "${pypiurl}/z/zc.buildout/zc.buildout-${buildoutVersion}.tar.gz"; md5 = buildoutHash; };
  buildoutDumpReq = pkgs.fetchurl { url = "${pypiurl}/b/buildout.dumprequirements/buildout.dumprequirements-${buildoutDumpReqVersion}.tar.gz"; md5 = buildoutDumpReqHash; };
  wheel = pkgs.fetchurl { url = "${pypiurl}/w/wheel/wheel-${wheelVersion}.tar.gz"; md5 = wheelHash; };
  bootstrap = pkgs.stdenv.mkDerivation {
    name = "pypi2nix-bootstrap";
    src = pip;
    buildInputs = [ pkgs.which pkgs.python pkgs.makeWrapper ];
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

      printf "#!${pkgs.python}/bin/python\nimport sys, pip; sys.exit(pip.main())" > $out/bin/pip
      chmod +x $out/bin/pip
    '';
  };

  pypi2nix_bootstrap = import ./bootstrap.nix {};

in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-py2txt";
  __noChroot = true;

  buildInputs = [
    pypi2nix_bootstrap pkgs.stdenv
  ] ++ (map (name: builtins.getAttr name pkgs) extraBuildInputs);

  buildCommand = (
    pkgs.lib.optionalString (cache != null) ''
    ''
  ) + ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir $out

    export PYTHONPATH=${bootstrap}/base

    pip wheel ${path} --wheel-dir ${cache} --find-links ${cache}
    pip install ${path} --find-links ${cache} --target $out/wheelhouse --no-index

    PYTHONPATH=$PYTHONPATH:$out/wheelhouse pip freeze > $out/requirements.txt
  '';
}
