{ stdenv, fetchurl, unzip, which, makeWrapper, python
}:

let
  deps = import ./deps.nix { inherit fetchurl; };
  wrappedPip = ''
    #!${stdenv.shell}

    exec python -m pip "$@"
  '';
in
  stdenv.mkDerivation {
    name = "pypi2nix-bootstrap";
    src = deps.pip;
    buildInputs = [ which python makeWrapper ];
    installPhase = ''

      mkdir -p $out/bin $out/index

      cp ${deps.pipWhl} $out/index/pip-${deps.pipVersion}-py2.py3-none-any.whl
      cp ${deps.setuptoolsWhl} $out/index/setuptools-${deps.setuptoolsVersion}-py2.py3-none-any.whl
      cp ${deps.wheel} $out/index/wheel-${deps.wheelVersion}.tar.gz

      mkdir tmp
      mv src/pip tmp/
      cd tmp

      python -c "import sys, pip._internal; sys.exit(pip._internal.main(['install', '--force-reinstall', '--upgrade', 'pip', 'setuptools', '--no-index', '--find-links=file://$out/index', '-v', '--target', '$out/base']))"
      PYTHONPATH=$out/base python -c "import sys, pip._internal; sys.exit(pip._internal.main(['install', '--force-reinstall', '--upgrade', 'wheel', '--no-index', '--find-links=file://$out/index', '-v', '--target', '$out/base']))"

      echo -e '${wrappedPip}' > $out/bin/pip

      sed -i -e "s|\[egg_info.writers\]|\[egg_info.writers\]\nsetup_requires.txt = setuptools.command.egg_info:write_setup_requirements|" $out/base/setuptools-${deps.setuptoolsVersion}.dist-info/entry_points.txt

      sed -i -e "s|data = io.StringIO()|data = six.StringIO()|" $out/base/setuptools/command/egg_info.py
      python -m compileall -f $out/base/setuptools/command/egg_info.py

      sed -i -e "s|zinfo = ZipInfo(arcname or filename, date_time=get_zipinfo_datetime(st.st_mtime))|zinfo = ZipInfo(arcname or filename, date_time=(1980,1,1,0,0,0))|" $out/base/wheel/wheelfile.py
      python -m compileall -f $out/base/wheel/wheelfile.py

      chmod +x $out/bin/*
    '';
  }
