{ requirements_files
, project_tmp_dir
, cache_dir
, wheelhouse_dir
, python_version
, extra_build_inputs ? []
}:

let
  pkgs = import <nixpkgs> {};
  python = builtins.getAttr python_version pkgs;
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper python;
  };
in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";

  buildInputs = [
    pypi2nix_bootstrap pkgs.unzip pkgs.gitAndTools.git
  ] ++ (map (name: pkgs.lib.getAttrFromPath
    (pkgs.lib.splitString "." name) pkgs) extra_build_inputs);

  shellHook = ''
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
    export PYTHONPATH=${pypi2nix_bootstrap}/base
    export LANG=en_US.UTF-8

    PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH pip wheel ${builtins.concatStringsSep" "(map (x: "-r ${x} ") requirements_files)} --no-binary :all: --wheel-dir ${project_tmp_dir} --find-links ${cache_dir}

    cd ${wheelhouse_dir}
    for file in ${project_tmp_dir}/*; do
      unzip -qo $file
    done

    cp -Rf ${project_tmp_dir}/* ${cache_dir}
  '';
}
