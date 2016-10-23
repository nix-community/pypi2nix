{ requirements_files
, project_dir
, download_cache_dir
, wheel_cache_dir
, pip_build_dir
, python_version
, extra_build_inputs ? []
, setup_requires ? []
}:

let

  pkgs = import <nixpkgs> {};

  python = builtins.getAttr python_version pkgs;

  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    inherit python;
  };

  numpySiteCfg = pkgs.lib.optionalString
    (
      (builtins.elem "numpy" setup_requires) &&
      (builtins.elem "blas" extra_build_inputs)
    )
    ''
      cat << EOF > $HOME/.numpy-site.cfg
      [openblas]
      include_dirs = ${pkgs.blas}/include
      library_dirs = ${pkgs.blas}/lib
      EOF
    '';

  scriptRequires = pkgs.lib.optionalString ((builtins.length setup_requires) > 0) ''
      mkdir -p ${project_dir}/setup_requires
      PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH \
        pip install \
          ${builtins.concatStringsSep" "(setup_requires)} \
          --target=${project_dir}/setup_requires \
          --find-links ${wheel_cache_dir} \
          --cache-dir ${download_cache_dir} \
          --build ${pip_build_dir} \
          --no-binary :all: 
    '';

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
    export HOME=${project_dir}

    ${numpySiteCfg}
    ${scriptRequires}
    export SOURCE_DATE_EPOCH=315532800

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
