{ pkgs, python }:

self: super: {

  "sentry" = python.overrideDerivation super."sentry" (old: {
    patchPhase = ''
     sed -i -e "s|Pillow>=3.2.0,<3.3.0|Pillow|" setup.py
    '';
  });

}
