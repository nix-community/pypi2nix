{ buildPythonPackage, deps, pyparsing, six }:
buildPythonPackage {
  name = "packaging-${deps.packaging.version}";
  src = deps.packaging.src;
  format = deps.packaging.format;
  propagatedBuildInputs = [ pyparsing six ];
}
