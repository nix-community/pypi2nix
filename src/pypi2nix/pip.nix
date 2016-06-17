{ requirements
, cache
, wheelhouse
, extraBuildInputs ? []
, pythonVersion ? "python27"
}:

let
  pkgs = import <nixpkgs> {};
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    python = builtins.getAttr pythonVersion pkgs;
  };
in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip";

  buildInputs = [
    pypi2nix_bootstrap pkgs.unzip pkgs.gitAndTools.git
  ] ++ (map (name: pkgs.lib.getAttrFromPath
    (pkgs.lib.splitString "." name) pkgs) extraBuildInputs);

  shellHook = ''
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
    export PYTHONPATH=${pypi2nix_bootstrap}/base

    PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH pip wheel -r ${requirements} --no-binary :all: --wheel-dir ${cache} --find-links ${cache}
    PYTHONPATH=${cache}:${pypi2nix_bootstrap}/extra:$PYTHONPATH pip freeze > ./requirements.txt

    cd ${wheelhouse}
    for file in ${cache}/*; do
      unzip -qo $file
    done
  '';
}
