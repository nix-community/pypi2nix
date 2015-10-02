{ cfg
, cache ? "$out/cache"
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
    pypi2nix_bootstrap pkgs.unzip
  ] ++ (map (name: builtins.getAttr name pkgs) extraBuildInputs);

  buildCommand = ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir -p $out/cache $out/wheelhouse

    export PYTHONPATH=${pypi2nix_bootstrap}/base


    mkdir tmp
    cp -R `dirname ${cfg}`/* tmp

    cat <<EOF > tmp/.pypi2nix.cfg
    [buildout]
    extends = ${cfg}
    download-cache = cache
    eggs-directory = eggs
    extensions = buildout.requirements
    dump-requirements-file = $out/requirements.txt
    overwrite-requirements-file = true
    EOF

    PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH buildout -c tmp/.pypi2nix.cfg

    for file in tmp/cache/dist/*; do
      PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH pip wheel $file --wheel-dir ${cache} --no-deps
    done

    cd $out/wheelhouse
    for file in ${cache}/*; do
      unzip -qo $file
    done
  '';
}

