{ requirements_files
, project_dir
, download_cache_dir
, wheel_cache_dir
, python_version
, extra_build_inputs ? []
, extra_env ? ""
, setup_requires ? []
, wheels_cache ? []
, pkgs
}:

let

  python = builtins.getAttr python_version pkgs;

  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    inherit python;
  };

in pkgs.lib.makeOverridable pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";

  buildInputs = with pkgs; [
    python
    pypi2nix_bootstrap
    unzip
    gitAndTools.git
    mercurial
  ] ++ (pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales)
    ++ (map (name: pkgs.lib.getAttrFromPath
          (pkgs.lib.splitString "." name) pkgs) extra_build_inputs);

  shellHook = ''
    set -e
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export PYTHONPATH=${pypi2nix_bootstrap}/base
    export PIP_DOWNLOAD_CACHE=${download_cache_dir}
    export LANG=en_US.UTF-8
    export HOME=${project_dir}
    export SOURCE_DATE_EPOCH=315532800
    export PYPI2NIX_BOOTSTRAP="${pypi2nix_bootstrap}"

    mkdir -p \
      ${project_dir}/build \
      ${project_dir}/src-download \
      ${project_dir}/src-wheel \
      ${project_dir}/wheel \
      ${project_dir}/wheelhouse
  '';
}
