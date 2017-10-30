{ buildPythonPackage, deps }:
buildPythonPackage {
  name = "pyparsing-${deps.pyparsing.version}";
  src = deps.pyparsing.src;
  format = deps.pyparsing.format;
}
