{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, extra_env
, wheels_cache
, requirements_files
, editable_sources_directory
, wheels_dir
, build_directory
, sources
}:

with builtins;

let
  pip_base = import ./base.nix {
    inherit project_dir download_cache_dir python_version extra_build_inputs;
  };
  sources_directories_links =
    concatStringsSep " " (map (x: "--find-links file://${x}") sources);
  find_directory_link = directory: "--find-links ${directory}";
  links = sources ++ wheels_cache ++ [wheels_dir];
in
pip_base.override( old: {
  shellHook = old.shellHook + ''
    ${extra_env} pip wheel \
      ${concatStringsSep " " (map find_directory_link links)} \
      ${concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --src ${editable_sources_directory} \
      --wheel-dir ${wheels_dir} \
      --no-index \
      --prefer-binary
  '';
})
