{ buildPythonPackage, deps }:
buildPythonPackage {
  name = "pip-${deps.pip.version}";
  src = deps.pip.src;
  format = deps.pip.format;
  doCheck = false;
}
