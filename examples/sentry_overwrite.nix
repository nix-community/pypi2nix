{ pkgs, self, generated, pythonPackages}:
let
  inherit (pkgs.lib) overrideDerivation;
  inherit (pythonPackages) buildPythonPackage python;
in {
  "lxml" = overrideDerivation generated."lxml" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pkgs.libxml2 pkgs.libxslt ];
  });
  "cffi" = overrideDerivation generated."cffi" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pkgs.libffi ];
  });
  "cryptography" = overrideDerivation generated."cryptography" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pkgs.libffi pkgs.openssl ];
  });
  "django-bitfield" = overrideDerivation generated."django-bitfield" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pkgs.pythonPackages.nose ];
  });
  "pytest-django" = overrideDerivation generated."pytest-django" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ self."setuptools_scm" self."six" ];
    patchPhase = ''
      sed -i -e "s|'setuptools_scm==1.8.0'||" setup.py
    '';
  });
  "ua-parser" = overrideDerivation generated."ua-parser" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pythonPackages.pyyaml ];
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ self."PyYAML" ];
    patchPhase = ''
      sed -i -e "s|if not os.path.exists(yaml_src):|if False:|"  setup.py
      sed -i -e "s|shutil.copy2(yaml_src, yaml_dest)||" setup.py
    '';
  });
  "PyYAML" = overrideDerivation generated."PyYAML" (old: {
    nativeBuildInputs = old.nativeBuildInputs ++ [ pkgs.pyrex pkgs.libyaml ];
  });


  "setuptools_scm" = buildPythonPackage rec {
    name = "setuptools_scm-1.7.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/source/s/setuptools_scm/${name}.tar.gz";
      md5 = "d0423feeabda9c6a869d963cdc397d64";
    };
    buildInputs = [ self."pip" ];
    preBuild = ''
      ${python.interpreter} setup.py egg_info
    '';
  };
  "pip" = buildPythonPackage rec {
    name = "pip-7.1.2";
    src = pkgs.fetchurl {
      url = "http://pypi.python.org/packages/source/p/pip/${name}.tar.gz";
      md5 = "3823d2343d9f3aaab21cf9c917710196";
    };
    doCheck = false;
  };
}
