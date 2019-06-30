{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, requirements_files
, target_directory
, wheel_cache_dir
, sources_directories
}:
let
  pip_base = import ./base.nix {
    inherit project_dir download_cache_dir python_version extra_build_inputs;
  };
  sources_directories_links =
    with builtins;
    concatStringsSep " " (map (x: "--find-links file://${x}") sources_directories);
in
pip_base.override( old: {
  shellHook = old.shellHook + ''
    pip install \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --target=${target_directory} \
      --find-links file://${wheel_cache_dir} \
      ${sources_directories_links} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --find-links file://${project_dir}/wheel \
      --find-links file://${download_cache_dir} \
      --no-index
  '';
})
