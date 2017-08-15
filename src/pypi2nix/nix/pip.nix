{ buildPythonPackageNoPip, python, deps, wheel }:
buildPythonPackageNoPip {
  name = "pip-${deps.pip.version}";
  src = deps.pip.src;
  format = deps.pip.format;
  installFlags = ["-U"];
  buildInputs = [ wheel ];
  patchPhase = ''
    mkdir -p $out/tmp/${python.sitePackages}
    export PYTHONPATH=$out/tmp/${python.sitePackages}:$PYTHONPATH
    export PATH=$out/tmp/bin:$PATH
    python setup.py install --prefix=$out/tmp
    installPhase=$(echo "$installPhase" | sed 's|.*/pip install|pip install|')
  '';
  fixupPhase = ''
    rm -rf $out/tmp
  '';
  doCheck = false;
}
