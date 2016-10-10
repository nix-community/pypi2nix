{ requirements_files
, project_dir
, download_cache_dir
, wheel_cache_dir
, pip_build_dir
, python_version
, extra_build_inputs ? []
}:

let
  pkgs = import <nixpkgs> {};
  python = builtins.getAttr python_version pkgs;
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    inherit python;
  };
in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";

  buildInputs = with pkgs; [
    pypi2nix_bootstrap
    unzip
    gitAndTools.git
  ] ++ (pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales)
    ++ (map (name: pkgs.lib.getAttrFromPath
          (pkgs.lib.splitString "." name) pkgs) extra_build_inputs);

  shellHook = ''
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export PYTHONPATH=${pypi2nix_bootstrap}/base
    export PIP_DOWNLOAD_CACHE=${download_cache_dir}
    export LANG=en_US.UTF-8

    mkdir -p ${project_dir}/wheel ${project_dir}/wheelhouse

    PYTHONPATH=${pypi2nix_bootstrap}/extra:${project_dir}/setup_requires:$PYTHONPATH \
      pip wheel \
        ${builtins.concatStringsSep" "(map (x: "-r ${x} ") requirements_files)} \
        --wheel-dir ${project_dir}/wheel \
        --find-links ${wheel_cache_dir} \
        --cache-dir ${download_cache_dir} \
        --build ${pip_build_dir} \
        --no-binary :all: 
    RETVAL=$?
    rm -rf ${pip_build_dir}/*
    [ $RETVAL -ne 0 ] && exit $RETVAL

    cd ${project_dir}/wheelhouse
    for file in ${project_dir}/wheel/*; do
      unzip -qo $file
    done

    cp -Rf ${project_dir}/wheel/* ${wheel_cache_dir}

    PYTHONPATH=${project_dir}/wheelhouse:$PYTHONPATH pip freeze > ${project_dir}/requirements.txt

  '';
}
