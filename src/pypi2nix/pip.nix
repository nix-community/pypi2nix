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

  blas = pkgs.openblasCompat;

in pip_base.override( old: {
  shellHook = old.shellHook + ''
    echo ""
    echo "==================================================================="
    echo "download source distributions to: ${download_cache_dir}"
    echo "==================================================================="
    echo ""
    ${extra_env} pip download \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --find-links file://${download_cache_dir} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --no-binary :all:

    rm -rf ${project_dir}/build

    echo ""
    echo "==================================================================="
    echo "create wheels from source distributions without going online"
    echo "==================================================================="
    echo ""
    ${extra_env} pip wheel \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      ${builtins.concatStringsSep " " (map (x: "--find-links ${x} ") wheels_cache)} \
      --find-links file://${wheel_cache_dir} \
      --find-links file://${download_cache_dir} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --no-index

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
