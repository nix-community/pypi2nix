{ cfg 
, extraBuildInputs ? []
}:

let

  pkgs = import <nixpkgs> {};
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper python;
  };

in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-cfg2txt";
  __noChroot = true;

  buildInputs = [
    pypi2nix_bootstrap pkgs.stdenv
  ] ++ (map (name: builtins.getAttr name pkgs) extraBuildInputs);

  buildCommand = ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir -p $out/cache $out/eggs

    export PYTHONPATH=${pypi2nix_bootstrap}/base:${pypi2nix_bootstrap}/extra


    mkdir tmp
    cp -R `dirname ${cfg}`/* tmp

    cat <<EOF > tmp/.pypi2nix.cfg
    [buildout]
    extends = ${cfg}
    download-cache = $out/cache
    eggs-directory = $out/eggs
    extensions = buildout.requirements
    dump-requirements-file = $out/requirements.txt
    overwrite-requirements-file = true
    EOF

    buildout -c tmp/.pypi2nix.cfg
  '';
}

