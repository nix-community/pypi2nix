{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, requirements_files
, target_directory
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
      ${sources_directories_links} \
      --find-links file://${project_dir}/wheel \
      --no-index
  '';
})
