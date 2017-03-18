{ pkgs, python }:

let
  blas = pkgs.openblasCompat;
  lib = pkgs.lib;
in

self: super:
let
  is_numpy_dep = drv:
    lib.hasSuffix
    ("numpy-" + (builtins.parseDrvName drv).version)
    (builtins.parseDrvName drv).name ;
in {

   "scipy" = python.overrideDerivation super."scipy" (old: {
      buildInputs =
        ( builtins.filter
          (drv: ! (is_numpy_dep drv))
          old.buildInputs
        )++ [ pkgs.gfortran ];
      propagatedBuildInputs = old.propagatedBuildInputs ++ [ blas self."numpy" ];
      preBuild = ''
        cat << EOF > site.cfg
        [openblas]
        include_dirs = ${blas}/include
        library_dirs = ${blas}/lib
        EOF
      '';
   });

   "numpy" = python.overrideDerivation super."numpy" (old: {
      buildInputs = old.buildInputs ++ [ pkgs.gfortran ];
      propagatedBuildInputs = old.propagatedBuildInputs ++ [ blas ];
      preBuild = ''
        cat << EOF > site.cfg
        [openblas]
        include_dirs = ${blas}/include
        library_dirs = ${blas}/lib
        EOF
      '';
   });

}
