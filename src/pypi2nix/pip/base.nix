{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
}:

let
  pkgs = import <nixpkgs> {};
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    inherit python;
  };
  python = builtins.getAttr python_version pkgs;
  extra_build_inputs_derivations = (map
    (name: pkgs.lib.getAttrFromPath (pkgs.lib.splitString "." name) pkgs)
    extra_build_inputs
  );

in pkgs.lib.makeOverridable pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";

  buildInputs = with pkgs; [
    python
    pypi2nix_bootstrap
    unzip
    gitAndTools.git
    mercurial
  ] ++ extra_build_inputs_derivations ++
    (pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales);


  shellHook = ''
    set -e
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export PYTHONPATH=${pypi2nix_bootstrap}/base:${project_dir}/lib
    export LANG=en_US.UTF-8
    export HOME=${project_dir}
    export SOURCE_DATE_EPOCH=315532800
    export PYPI2NIX_BOOTSTRAP="${pypi2nix_bootstrap}"

    export PIP_DOWNLOAD_CACHE=${download_cache_dir}

    mkdir -p \
      ${project_dir}/build \
      ${project_dir}/src \
      ${project_dir}/wheel \
      ${project_dir}/wheelhouse
  '';
}
