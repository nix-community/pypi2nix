{ pkgs, python }:

self: super: {

  "Lektor" = python.overrideDerivation super."Lektor" (old: {
    patchPhase = ''
      sed -i -e "s|requests\[security\]|requests|" setup.py
    '';
  });

}
