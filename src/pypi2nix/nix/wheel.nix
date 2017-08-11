{ python, buildPythonPackage, deps }:
buildPythonPackage {
  name = "wheel";
  src = deps.wheel.src;
  format = deps.wheel.format;
  doCheck = false;
  installFlags = ["-U"];
  patchPhase = ''
    sed -i "s|'test':.*||" setup.py
  '';
}
