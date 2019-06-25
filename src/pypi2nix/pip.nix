args @
{ requirements_files
, project_dir
, download_cache_dir
, wheel_cache_dir
, python_version
, extra_build_inputs ? []
, extra_env ? ""
, setup_requires ? []
, wheels_cache ? []
}:

let
  pkgs = import <nixpkgs> {};
  extra_build_inputs_derivations = (map
    (name: pkgs.lib.getAttrFromPath (pkgs.lib.splitString "." name) pkgs)
    extra_build_inputs
  );

  pip_base = import pip/base.nix {
    inherit project_dir download_cache_dir pkgs;
    python = builtins.getAttr python_version pkgs;
    extra_build_inputs = extra_build_inputs_derivations;
  };

  blas = pkgs.openblasCompat;

  numpySiteCfg = pkgs.lib.optionalString
    (
      (builtins.elem "numpy" setup_requires)
    )
    ''
      cat << EOF > $HOME/.numpy-site.cfg
      [openblas]
      include_dirs = ${blas}/include
      library_dirs = ${blas}/lib
      EOF
      echo ""
      echo "==================================================================="
      echo "content of ~/.numpy-site.cfg"
      echo "-------------------------------------------------------------------"
      cat $HOME/.numpy-site.cfg
      echo "==================================================================="
      echo ""
    '';

  scriptRequires = pkgs.lib.optionalString ((builtins.length setup_requires) > 0) ''
      mkdir -p ${project_dir}/setup_requires

      echo ""
      echo "==================================================================="
      echo "(setup_requires) download source distributions to: ${download_cache_dir}"
      echo "==================================================================="
      echo ""
      ${extra_env} pip download \
        ${builtins.concatStringsSep " " setup_requires} \
        ${builtins.concatStringsSep " " (map (x: "-c ${x} ") requirements_files)} \
        --dest ${download_cache_dir} \
        --src ${project_dir}/src-download \
        --build ${project_dir}/build \
        --find-links file://${download_cache_dir} \
        --no-binary :all: \
        --exists-action w

      rm -rf ${project_dir}/build

      echo ""
      echo "==================================================================="
      echo "(setup_requires) create wheels from source distributions without going online"
      echo "==================================================================="
      echo ""
      ${extra_env} pip wheel \
        ${builtins.concatStringsSep " " setup_requires} \
        --src ${project_dir}/src-wheel \
        --build ${project_dir}/build \
        --wheel-dir ${project_dir}/wheel \
        ${builtins.concatStringsSep " " (map (x: "--find-links ${x} ") wheels_cache)} \
        --find-links file://${wheel_cache_dir} \
        --find-links file://${download_cache_dir} \
        --find-links file://$PYPI2NIX_BOOTSTRAP/index \
        --no-index

      for file in ${project_dir}/wheel/*; do
        cp -f $file ${wheel_cache_dir}
      done

      echo ""
      echo "==================================================================="
      echo "(setup_requires) install setup_requires from wheels"
      echo "==================================================================="
      echo ""
      pip install \
        ${builtins.concatStringsSep " " setup_requires} \
        --target=${project_dir}/setup_requires \
        --find-links file://${wheel_cache_dir} \
        --find-links file://$PYPI2NIX_BOOSTRAP/index \
        --no-index
    '';

in pip_base.override( old: {
  shellHook = old.shellHook + ''
    ${numpySiteCfg}
    ${scriptRequires}

    echo ""
    echo "==================================================================="
    echo "download source distributions to: ${download_cache_dir}"
    echo "==================================================================="
    echo ""
    PYTHONPATH=${project_dir}/setup_requires:$PYTHONPATH \
      ${extra_env} pip download \
        ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
        --dest ${download_cache_dir} \
        --src ${project_dir}/src-download \
        --build ${project_dir}/build \
        --find-links file://${download_cache_dir} \
        --find-links file://$PYPI2NIX_BOOTSTRAP/index \
        --no-binary :all: \
        --exists-action w

    rm -rf ${project_dir}/build

    echo ""
    echo "==================================================================="
    echo "create wheels from source distributions without going online"
    echo "==================================================================="
    echo ""
    PYTHONPATH=${project_dir}/setup_requires:$PYTHONPATH \
      ${extra_env} pip wheel \
        ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
        --wheel-dir ${project_dir}/wheel \
        --src ${project_dir}/src-wheel \
        --build ${project_dir}/build \
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
