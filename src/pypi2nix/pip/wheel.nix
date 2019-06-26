{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, extra_env
, wheels_cache
, requirements_files
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
    ${extra_env} pip wheel \
      ${builtins.concatStringsSep " " (map (x: "--find-links ${x} ") wheels_cache)} \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --find-links file://${wheel_cache_dir} \
      --find-links file://${download_cache_dir} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --no-index
  '';
})
