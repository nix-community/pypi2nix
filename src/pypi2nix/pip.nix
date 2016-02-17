{ requirements
, cache ? "$out/cache"
, extraBuildInputs ? []
}:

let
  pkgs = import <nixpkgs> {};
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper python;
  };
in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";
  __noChroot = true;


  buildInputs = [
    pypi2nix_bootstrap pkgs.unzip pkgs.gitAndTools.git
  ] ++ (map (name: pkgs.lib.getAttrFromPath
    (pkgs.lib.splitString "." name) pkgs) extraBuildInputs);

  buildCommand = ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir -p $out/wheelhouse

    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
    export PYTHONPATH=${pypi2nix_bootstrap}/base

    echo "${requirements}" > requirements.txt

    PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH pip wheel -r requirements.txt --wheel-dir ${cache} --find-links ${cache}
    PYTHONPATH=${cache}:${pypi2nix_bootstrap}/extra:$PYTHONPATH pip freeze > $out/requirements.txt

    cd $out/wheelhouse
    for file in ${cache}/*; do
      unzip -qo $file
    done
  '';
}
