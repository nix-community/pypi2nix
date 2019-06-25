{ project_dir
, download_cache_dir
, python
, extra_build_inputs
, pkgs
}:

let
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
  ] ++ extra_build_inputs ++
    (pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales);


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
