{ pkgs, python }:

self: super: {

   "cffi" = python.overrideDerivation super."cffi" (old: {
      buildInputs = old.buildInputs ++ [ pkgs.libffi ];
   });

   "cryptography" = python.overrideDerivation super."cryptography" (old: {
      doCheck = false;
      buildInputs = old.buildInputs ++ [ pkgs.openssl ];
   });

   "Lektor" = python.overrideDerivation super."Lektor" (old: {
      propagatedBuildInputs = old.propagatedBuildInputs ++ (builtins.attrValues python.modules);
   });

}
