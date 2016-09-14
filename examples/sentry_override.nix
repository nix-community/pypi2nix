{ pkgs, python }:

self: super: {

  "sentry" = python.overrideDerivation super."sentry" (old: {
    preConfigure = ''
      sed -i \
        -e "s|'pytest-django>=2.9.1,<2.10.0',|'pytest-django',|" \
        -e "s|'Pillow>=3.2.0,<3.3.0',|'Pillow',|" \
        setup.py
    '';
  });

  "pytest-django" = python.overrideDerivation super."pytest-django" (old: {
    preConfigure = ''
      sed -i -e "s|setup_requires=\['setuptools_scm==1.8.0'\],|setup_requires=\[\],|" setup.py
    '';
  });

  "django-bitfield" = python.overrideDerivation super."django-bitfield" (old: {
    buildInputs = old.buildInputs ++ [ self."nose" ];
  });

  "python-utils" = python.overrideDerivation super."python-utils" (old: {
    buildInputs = old.buildInputs ++ [ self."pytest-runner" ];
  });

  "pytest-runner" = python.overrideDerivation super."pytest-runner" (old: {
    buildInputs = old.buildInputs ++ [ self."setuptools-scm" ];
  });

  "progressbar2" = python.overrideDerivation super."progressbar2" (old: {
    buildInputs = old.buildInputs ++ [ self."pytest-runner" ];
  });

  "ua-parser" = python.overrideDerivation super."ua-parser" (old: {
    preConfigure = ''
      sed -i -e "s|setup_requires=\['pyyaml'\],|setup_requires=\[\],|" setup.py
    '';
  });

}
