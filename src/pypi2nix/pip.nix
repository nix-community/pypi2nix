{ requirements_files
, project_dir
, download_cache_dir
, wheel_cache_dir
, python_version
, extra_build_inputs ? []
, extra_env ? ""
, wheels_cache ? []
}:

let
  pkgs = import <nixpkgs> {};
  extra_build_inputs_derivations = (map
    (name: pkgs.lib.getAttrFromPath (pkgs.lib.splitString "." name) pkgs)
    extra_build_inputs
  );
  python = builtins.getAttr python_version pkgs;
  pip_base = import pip/base.nix {
    inherit project_dir download_cache_dir pkgs python;
    extra_build_inputs = extra_build_inputs_derivations;
  };

in pip_base.override( old: {
  shellHook = old.shellHook + ''
    RETVAL=$?
    for file in ${project_dir}/wheel/*; do
      cp -f $file ${wheel_cache_dir}
    done
    [ $RETVAL -ne 0 ] && exit $RETVAL

    pushd ${project_dir}/wheelhouse
    for file in ${project_dir}/wheel/*; do
      unzip -qo $file
    done
    popd

    PYTHONPATH=${project_dir}/wheelhouse:$PYTHONPATH pip freeze > ${project_dir}/requirements.txt

    python -c "import json; from setuptools._vendor.packaging.markers import default_environment; print(json.dumps(default_environment(), indent=2, sort_keys=True))" > ${project_dir}/default_environment.json
  '';
})
