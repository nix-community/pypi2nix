{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, requirements_files
, target_directory
, wheel_cache_dir
}:
let
  pkgs = import <nixpkgs> {};
  extra_build_inputs_derivations = (map
    (name: pkgs.lib.getAttrFromPath (pkgs.lib.splitString "." name) pkgs)
    extra_build_inputs
  );
  python = builtins.getAttr python_version pkgs;
  pip_base = import ./base.nix {
    inherit project_dir download_cache_dir pkgs;
    python = builtins.getAttr python_version pkgs;
    extra_build_inputs = extra_build_inputs_derivations;
  };
in
pip_base.override( old: {
  shellHook = old.shellHook + ''
    pip install \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --target=${target_directory} \
      --find-links file://${wheel_cache_dir} \
      --find-links file://$PYPI2NIX_BOOSTRAP/index \
      --find-links file://${project_dir}/wheel \
      --no-index
  '';
})
