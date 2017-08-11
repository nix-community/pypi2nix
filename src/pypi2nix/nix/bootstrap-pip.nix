{ stdenv, python, deps, makeWrapper }:
stdenv.mkDerivation {
  name = "bootstrap-pip";
  srcs = [
    deps.setuptools.src
    deps.wheel.src
    deps.pip.src
  ];
  sourceRoot = ".";
  postUnpack = ''
    mkdir -p $out/${python.sitePackages}
    cp -R pip*/* $out/${python.sitePackages}/
    cp -R setuptools*/* $out/${python.sitePackages}/
    cp -R wheel*/* $out/${python.sitePackages}/ # hey emacs: */
  '';
  buildInputs = [ python makeWrapper ];
  installPhase = ''
    mkdir $out/bin
    echo '#!${python.interpreter}' > $out/bin/pip
    echo 'import sys;from pip import main' >> $out/bin/pip
    echo 'sys.exit(main())' >> $out/bin/pip
    chmod +x $out/bin/pip
    # wrap binaries with PYTHONPATH
    export BOOTSTRAP_PYTHON_PATH="$out/${python.sitePackages}/"
    for f in $out/bin/*; do  # hey emacs: */
      wrapProgram $f --prefix PYTHONPATH ":" $BOOTSTRAP_PYTHON_PATH
    done
  '';
}
