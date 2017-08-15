{ python, buildPythonPackageNoWheel, deps }:
buildPythonPackageNoWheel {
  name = "wheel";
  src = deps.wheel.src;
  format = deps.wheel.format;
  doCheck = false;
  installFlags = ["-U"];
  patchPhase = ''
    sed -i "s|'test':.*||" setup.py
    mkdir -p $out/tmp/${python.sitePackages}
    export PYTHONPATH=$out/tmp/${python.sitePackages}:$PYTHONPATH
    python setup.py install --prefix=$out/tmp
  '';
  fixupPhase = ''
    rm -rf $out/tmp
  '';
}
