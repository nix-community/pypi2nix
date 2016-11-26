{ pkgs, python }:

let
  blas = pkgs.openblasCompat;
in

self: super: {

   "scipy" = python.overrideDerivation super."scipy" (old: {
      buildInputs = old.buildInputs ++ [ pkgs.gfortran ];
      propagatedBuildInputs = old.propagatedBuildInputs ++ [ blas super."numpy" ];
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
