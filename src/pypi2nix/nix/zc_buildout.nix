{ buildPythonPackage, deps }:
buildPythonPackage {
  name = "zc-buildout-${deps.zc_buildout.version}";
  src = deps.zc_buildout.src;
  format = deps.zc_buildout.format;
}
