{ pkgs, python }:

self: super: {

   "honcho" = python.overrideDerivation super."cffi" (old: {
      src = pkgs.fetchFromGitHub {
        owner = "nickstenning";
        repo = "honcho";
        rev = "v0.7.1";
        sha256 = "0xzrby0dy77wh29pk1nz20ic1fqw4l0cmdz8vq3iv2yx5y7nnb4l";
      };
   });

   "cffi" = python.overrideDerivation super."cffi" (old: {
      buildInputs = old.buildInputs ++ [ pkgs.libffi ];
   });

   "cryptography" = python.overrideDerivation super."cryptography" (old: {
      doCheck = false;
      buildInputs = old.buildInputs ++ [ pkgs.openssl ];
   });

  "lxml" = python.overrideDerivation super."lxml" (old: {
    buildInputs = [ pkgs.libxml2 pkgs.libxslt ];
  });

  "psycopg2" = python.overrideDerivation super."psycopg2" (old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ pkgs.postgresql ];
  });

  "django-bitfield" = python.overrideDerivation super."django-bitfield" (old: {
    doCheck = false;
    buildInputs = [ python.pkgs.nose ];
  });

  "pytest-django" = python.overrideDerivation super."pytest-django" (old: {
    buildInputs = [ self."setuptools_scm" self."six" ];
    patchPhase = ''
      sed -i -e "s|'setuptools_scm==1.8.0'||" setup.py
    '';
  });

  "ua-parser" = python.overrideDerivation super."ua-parser" (old: {
    buildInputs = [ self."PyYAML" ];
    patchPhase = ''
      sed -i -e "s|if not os.path.exists(yaml_src):|if False:|"  setup.py
      sed -i -e "s|shutil.copy2(yaml_src, yaml_dest)||" setup.py
    '';
  });

  "PyYAML" = python.overrideDerivation super."PyYAML" (old: {
    buildInputs = [ pkgs.pyrex pkgs.libyaml ];
  });

  "setuptools_scm" = python.mkDerivation rec {
    name = "setuptools_scm-1.7.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/source/s/setuptools_scm/${name}.tar.gz";
      md5 = "d0423feeabda9c6a869d963cdc397d64";
    };
    buildInputs = [ self."pip" ];
    preBuild = ''
      ${python.interpreter.interpreter} setup.py egg_info
    '';
  };

  "pip" = python.mkDerivation rec {
    name = "pip-8.0.2";
    src = pkgs.fetchurl {
      url = "http://pypi.python.org/packages/source/p/pip/${name}.tar.gz";
      md5 = "3a73c4188f8dbad6a1e6f6d44d117eeb";
    };
    doCheck = false;
    # pip detects that we already have bootstrapped_pip "installed", so we need
    # to force it a little.
    installFlags = [ "--ignore-installed" ];
  };


}
