{ pkgs, python }:

self: super: {

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
       include_dirs = ${pkgs.openblasCompat}/include
       library_dirs = ${pkgs.openblasCompat}/lib
       EOF
     '';
     setupPyBuildFlags = [ "--fcompiler='gnu95'" ];
     passthru = {
       blas = pkgs.openblasCompat;
     };
  });

  "numpy" = python.overrideDerivation super."numpy" (old: {
      preConfigure = ''
        sed -i 's/-faltivec//' numpy/distutils/system_info.py
      '';
      preBuild = ''
        echo "Creating site.cfg file..."
        cat << EOF > site.cfg
        [openblas]
        include_dirs = ${pkgs.openblasCompat}/include
        library_dirs = ${pkgs.openblasCompat}/lib
        EOF
      '';
      passthru = {
        blas = pkgs.openblasCompat;
      };
  });

}
