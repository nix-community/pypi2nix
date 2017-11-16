{ stdenv, python, deps, ensureNewerSourcesHook }:
stdenv.mkDerivation {
  name = "setuptools-${deps.setuptools.version}";
  src = deps.setuptools.src;
  phases = [ "unpackPhase" "installPhase" ];
  buildInputs = [
    python
    (ensureNewerSourcesHook { year = "1980"; })
  ];
  installPhase = ''
    export PYTHONPATH=$PWD:$out/${python.sitePackages}
    mkdir -p $out/${python.sitePackages}/
    python bootstrap.py
    python setup.py install --prefix $out
  '';
}
