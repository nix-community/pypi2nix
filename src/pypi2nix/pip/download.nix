{ download_cache_dir
, extra_build_inputs
, project_dir
, python_version
, extra_env
, requirements_files
, constraint_files
, destination_directory
, editable_sources_directory
, build_directory
}:
let
  pip_base = import ./base.nix {
    inherit project_dir download_cache_dir python_version extra_build_inputs;
  };
  requirements_files_option =
    builtins.concatStringsSep " " (map (x: "-r ${x} ") requirements_files);
in
pip_base.override( old: {
  shellHook = old.shellHook + ''
    ${extra_env} pip download \
      ${requirements_files_option} \
      ${builtins.concatStringsSep " " (map (x: "-c ${x} ") constraint_files)} \
      --dest ${destination_directory} \
      --src ${editable_sources_directory} \
      --build ${build_directory} \
      --find-links file://${download_cache_dir} \
      --find-links file://$PYPI2NIX_BOOTSTRAP/index \
      --no-binary :all: \
      --exists-action w
  '';
})
