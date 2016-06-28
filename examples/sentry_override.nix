{ pkgs, python }:

self: super: {

#   "honcho" = python.overrideDerivation super."cffi" (old: {
#      src = pkgs.fetchFromGitHub {
#        owner = "nickstenning";
#        repo = "honcho";
#        rev = "v0.7.1";
#        sha256 = "0xzrby0dy77wh29pk1nz20ic1fqw4l0cmdz8vq3iv2yx5y7nnb4l";
#      };
#   });

#  "psycopg2" = python.overrideDerivation super."psycopg2" (old: {
#    propagatedBuildInputs = old.propagatedBuildInputs ++ [ pkgs.postgresql ];
#  });

#  "django-bitfield" = python.overrideDerivation super."django-bitfield" (old: {
#    doCheck = false;
#    buildInputs = [ python.pkgs.nose ];
#  });
#
#  "pytest-django" = python.overrideDerivation super."pytest-django" (old: {
#    buildInputs = [ self."setuptools_scm" self."six" ];
#    patchPhase = ''
#      sed -i -e "s|'setuptools_scm==1.8.0'||" setup.py
#    '';
#  });
#
#  "ua-parser" = python.overrideDerivation super."ua-parser" (old: {
#    buildInputs = [ self."PyYAML" ];
#    patchPhase = ''
#      sed -i -e "s|if not os.path.exists(yaml_src):|if False:|"  setup.py
#      sed -i -e "s|shutil.copy2(yaml_src, yaml_dest)||" setup.py
#    '';
#  });
#
#  "PyYAML" = python.overrideDerivation super."PyYAML" (old: {
#    buildInputs = [ pkgs.pyrex pkgs.libyaml ];
#  });
#
  "sentry" = python.overrideDerivation super."sentry" (old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ self."Pillow" ];
  });
#
#
#  "setuptools_scm" = python.mkDerivation rec {
#    name = "setuptools_scm-1.7.0";
#    src = pkgs.fetchurl {
#      url = "https://pypi.python.org/packages/source/s/setuptools_scm/${name}.tar.gz";
#      md5 = "d0423feeabda9c6a869d963cdc397d64";
#    };
#    buildInputs = [ self."pip" ];
#    preBuild = ''
#      ${python.interpreter.interpreter} setup.py egg_info
#    '';
#  };
#
#  "pip" = python.mkDerivation rec {
#    name = "pip-8.0.2";
#    src = pkgs.fetchurl {
#      url = "http://pypi.python.org/packages/source/p/pip/${name}.tar.gz";
#      md5 = "3a73c4188f8dbad6a1e6f6d44d117eeb";
#    };
#    doCheck = false;
#    # pip detects that we already have bootstrapped_pip "installed", so we need
#    # to force it a little.
#    installFlags = [ "--ignore-installed" ];
#  };

  "Pillow" = python.mkDerivation rec {
    name = "Pillow-3.2.0";
    src = pkgs.fetchurl {
      url = "mirror://pypi/P/Pillow/${name}.zip";
      sha256 = "1rddmdg8vzjccfa6ri8l9ja166sqlyjlih0b7ngca9rb8d5wai6c";
    };
    doCheck = false;
    buildInputs = [ pkgs.freetype pkgs.libjpeg pkgs.zlib pkgs.libtiff pkgs.libwebp pkgs.tcl pkgs.lcms2 ];
    preConfigure = let
      libinclude = pkg: ''"${pkg.out}/lib", "${pkg.dev}/include"'';
    in ''
      sed -i "setup.py" \
          -e 's|^FREETYPE_ROOT =.*$|FREETYPE_ROOT = ${libinclude pkgs.freetype}|g ;
              s|^JPEG_ROOT =.*$|JPEG_ROOT = ${libinclude pkgs.libjpeg}|g ;
              s|^ZLIB_ROOT =.*$|ZLIB_ROOT = ${libinclude pkgs.zlib}|g ;
              s|^LCMS_ROOT =.*$|LCMS_ROOT = _lib_include("${pkgs.libwebp}")|g ;
              s|^TIFF_ROOT =.*$|TIFF_ROOT = ${libinclude pkgs.libtiff}|g ;
              s|^TCL_ROOT=.*$|TCL_ROOT = _lib_include("${pkgs.tcl}")|g ;'
    '';
  };
}
