{ buildPythonPackage, deps, zc_buildout }:
buildPythonPackage {
  name = "zc.recipe.egg-${deps.zc_recipe_egg.version}";
  src = deps.zc_recipe_egg.src;
  format = deps.zc_recipe_egg.format;
  propagatedBuildInputs = [ zc_buildout ];
  doCheck = false;
}
