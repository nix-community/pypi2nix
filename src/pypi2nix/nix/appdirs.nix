{ buildPythonPackage, deps }:
buildPythonPackage {
  name = "appdirs-${deps.appdirs.version}";
  src = deps.appdirs.src;
  format = deps.appdirs.format;
}
