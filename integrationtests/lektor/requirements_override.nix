{ pkgs, python }:

self: super: {
  "lektor" = python.overrideDerivation super."lektor" (old: {
    patchPhase = ''
      sed -i -e "s|requests\[security\]|requests|" setup.py
    '';
  });

   "pip" = super."pip".overrideDerivation (old: {
     pipInstallFlags = ["--ignore-installed"];
   });
}
