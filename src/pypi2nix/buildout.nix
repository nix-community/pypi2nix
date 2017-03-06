{ buildout_file
, project_dir
, buildout_cache_dir
, python_version
, extra_build_inputs ? []
}:

let
  pkgs = import <nixpkgs> {};
  python = builtins.getAttr python_version pkgs;
  pypi2nix_bootstrap = import ./bootstrap.nix {
    inherit (pkgs) stdenv fetchurl unzip which makeWrapper;
    inherit python;
  };

in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-buildout";

  buildInputs = with pkgs; [
    pypi2nix_bootstrap
    unzip
    gitAndTools.git
  ] ++ (pkgs.lib.optional pkgs.stdenv.isLinux pkgs.glibcLocales)
    ++ (map (name: pkgs.lib.getAttrFromPath
          (pkgs.lib.splitString "." name) pkgs) extra_build_inputs);

  shellHook = ''
    export GIT_SSL_CAINFO="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
    export PYTHONPATH=${pypi2nix_bootstrap}/base
    export LANG=en_US.UTF-8
    export HOME=${project_dir}

    mkdir -p ${buildout_cache_dir}/download ${buildout_cache_dir}/eggs

    cat <<EOF > ${project_dir}/buildout.cfg
    [buildout]
    extends = ${buildout_file}
    extensions = buildout.requirements
    dump-requirements-file = ${project_dir}/buildout_requirements.txt
    overwrite-requirements-file = true

    download-cache = ${buildout_cache_dir}/download
    eggs-directory = ${buildout_cache_dir}/eggs

    parts-directorya = ${project_dir}/parts
    installed = ${project_dir}/.installed.cfg
    bin-directory = ${project_dir}/bin
    develop-eggs-directory = ${project_dir}/develop-eggs
    EOF

    cp ${project_dir}/buildout.cfg $PWD/pypi2nix.cfg

    PYTHONPATH=${pypi2nix_bootstrap}/extra:$PYTHONPATH buildout -vvv -c $PWD/pypi2nix.cfg

    rm $PWD/pypi2nix.cfg
  '';
}
