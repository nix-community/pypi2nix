{ stdenv, fetchurl, unzip, which, makeWrapper, python
}:

let
  deps = import ./deps.nix { inherit fetchurl; };
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

      ${python.interpreter} -c "import sys, pip._internal; sys.exit(pip._internal.main(['install', '--force-reinstall', '--upgrade', 'pip', 'setuptools', '--no-index', '--find-links=file://$out/index', '-v', '--target', '$out/base']))"
      PYTHONPATH=$out/base ${python.interpreter} -c "import sys, pip._internal; sys.exit(pip._internal.main(['install', '--force-reinstall', '--upgrade', 'wheel', '--no-index', '--find-links=file://$out/index', '-v', '--target', '$out/base']))"

      echo -e "#!${python.interpreter}\nimport sys, pip._internal; sys.exit(pip._internal.main())" > $out/bin/pip

      sed -i -e "s|\[egg_info.writers\]|\[egg_info.writers\]\nsetup_requires.txt = setuptools.command.egg_info:write_setup_requirements|" $out/base/setuptools-${deps.setuptoolsVersion}.dist-info/entry_points.txt
      sed -i -e "s|data = io.StringIO()|data = six.StringIO()|" $out/base/setuptools/command/egg_info.py
      python -m compileall -f $out/base/setuptools/command/egg_info.py

      chmod +x $out/bin/*
    '';
  }
