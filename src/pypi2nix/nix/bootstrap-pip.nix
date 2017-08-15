{ stdenv, python, deps, makeWrapper, ensureNewerSourcesHook
, include_wheel ? true
}:
stdenv.mkDerivation {
  name = "bootstrap-pip";
  include_wheel = if include_wheel then "yes" else "no";
  srcs = [
    deps.setuptools.src
    deps.wheel.src
    deps.pip.src
  ];
  sourceRoot = ".";
  postUnpack = ''
    mkdir -p $out/${python.sitePackages}
  '';
  buildInputs = [ python makeWrapper (ensureNewerSourcesHook { year="1980";}) ];
  installPhase = ''
    PYTHONPATH=$out/${python.sitePackages}
    pushd setuptools-*
    python bootstrap.py
    python setup.py install --prefix=$out
    popd
    if [ $include_wheel = "yes" ]; then
        pushd wheel-*
        python setup.py install --prefix=$out
        popd
    fi
    if [ -d pip ]; then
      pushd pip
    else
      pushd pip-*
    fi
    python setup.py install --prefix=$out
    popd
    rm $out/bin/*
    echo '#!${python.interpreter}' > $out/bin/pip
    echo 'import sys;from pip import main' >> $out/bin/pip
    echo 'sys.exit(main())' >> $out/bin/pip
    chmod +x $out/bin/pip
    # wrap binaries with PYTHONPATH
    export BOOTSTRAP_PYTHON_PATH="$out/${python.sitePackages}/"
    for f in $out/bin/*; do
      wrapProgram $f --prefix PYTHONPATH ":" $BOOTSTRAP_PYTHON_PATH
    done
  '';
}
