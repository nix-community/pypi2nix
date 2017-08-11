{ buildPythonPackage, deps, zc_buildout, zc_recipe_egg }:
buildPythonPackage {
  name = "buildout.requirements-${deps.buildout_requirements.version}";
  src = deps.buildout_requirements.src;
  format = deps.buildout_requirements.format;
  propagatedBuildInputs = [ zc_buildout zc_recipe_egg ];
  doCheck = false;
}
