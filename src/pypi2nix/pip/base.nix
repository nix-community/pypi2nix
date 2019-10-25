{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
}:

let
  pkgs = import <nixpkgs> {};
  python = builtins.getAttr python_version pkgs;
  pypi2nix_bootstrap = pkgs.callPackage ./bootstrap.nix {inherit python;};
  nixpkg_from_name = name:
    pkgs.lib.getAttrFromPath (pkgs.lib.splitString "." name) pkgs;
  extra_build_inputs_derivations = map nixpkg_from_name extra_build_inputs;
  locales = pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales;
in pkgs.lib.makeOverridable pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";
  buildInputs = with pkgs; [
    pypi2nix_bootstrap
    unzip
    gitAndTools.git
    mercurial
  ] ++ extra_build_inputs_derivations ++ locales;
  shellHook = ''
    set -e
    export TMPDIR=${project_dir}
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export PYTHONPATH=${project_dir}/lib
    export LANG=en_US.UTF-8
    export HOME=${project_dir}
    export SOURCE_DATE_EPOCH=315532800
    export PYPI2NIX_BOOTSTRAP="${pypi2nix_bootstrap}"
    export PIP_CACHE_DIR=${download_cache_dir}
    export PIP_EXISTS_ACTION="s"
  '';
}
