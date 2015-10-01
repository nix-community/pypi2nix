{ path
, extraBuildInputs ? []
, cache ? null
}:

let
  pkgs = import <nixpkgs> {};
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper python;
  };

in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-py2txt";
  __noChroot = true;

  buildInputs = [
    pypi2nix_bootstrap pkgs.stdenv
  ] ++ (map (name: builtins.getAttr name pkgs) extraBuildInputs);

  buildCommand = (
    pkgs.lib.optionalString (cache != null) ''
    ''
  ) + ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir $out

    export PYTHONPATH=${bootstrap}/base

    pip wheel ${path} --wheel-dir ${cache} --find-links ${cache}
    pip install ${path} --find-links ${cache} --target $out/wheelhouse --no-index

    PYTHONPATH=$PYTHONPATH:$out/wheelhouse pip freeze > $out/requirements.txt
  '';
}
