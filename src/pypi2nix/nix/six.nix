{ buildPythonPackage, deps }:
buildPythonPackage {
  name = "six";
  src = deps.six.src;
  format = deps.six.format;
}
