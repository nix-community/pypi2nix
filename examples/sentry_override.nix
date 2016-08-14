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

}
