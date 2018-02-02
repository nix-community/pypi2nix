{ pkgs, python }:

let
  blas = pkgs.openblasCompat;
  lib = pkgs.lib;
in

self: super: {

   "numpy" = python.overrideDerivation super."numpy" (old: {
      #patches = lib.optionals (python.hasDistutilsCxxPatch or false) [
      #  # See cpython 2.7 patches.
      #  # numpy.distutils is used by cython during it's check phase
      #  ./numpy-distutils-C++.patch
      #];
      preConfigure = ''
        sed -i 's/-faltivec//' numpy/distutils/system_info.py
      '';
      preBuild = ''
        echo "Creating site.cfg file..."
        cat << EOF > site.cfg
        [openblas]
        include_dirs = ${blas}/include
        library_dirs = ${blas}/lib
        EOF
      '';
      postInstall = ''
        ln -s $out/bin/f2py* $out/bin/f2py
      '';
      passthru = {
        blas = blas;
      };
   });

   "scipy" = python.overrideDerivation super."scipy" (old: {
      prePatch = ''
        rm scipy/linalg/tests/test_lapack.py
      '';
      preConfigure = ''
        sed -i '0,/from numpy.distutils.core/s//import setuptools;from numpy.distutils.core/' setup.py
      '';
      preBuild = ''
        echo "Creating site.cfg file..."
        cat << EOF > site.cfg
        [openblas]
        include_dirs = ${blas}/include
        library_dirs = ${blas}/lib
        EOF
      '';
      setupPyBuildFlags = [ "--fcompiler='gnu95'" ];
      passthru = {
        blas = blas;
      };

   });

}
