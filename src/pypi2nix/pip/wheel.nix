{ project_dir
, download_cache_dir
, python_version
, extra_build_inputs
, extra_env
, wheels_cache
, requirements_files
, wheel_cache_dir
, editable_sources_directory
, wheels_dir
, build_directory
, sources
}:
let
  pip_base = import ./base.nix {
    inherit project_dir download_cache_dir python_version extra_build_inputs;
  };
  sources_directories_links =
    with builtins;
    concatStringsSep " " (map (x: "--find-links file://${x}") sources);
in
pip_base.override( old: {
  shellHook = old.shellHook + ''
    ${extra_env} pip wheel \
      ${builtins.concatStringsSep " " (map (x: "--find-links ${x} ") wheels_cache)} \
      ${builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files)} \
      --src ${editable_sources_directory} \
      --wheel-dir ${wheels_dir} \
      --build ${build_directory} \
      ${sources_directories_links} \
      --find-links file://${wheel_cache_dir} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --no-index \
      --exists-action w
  '';
})
