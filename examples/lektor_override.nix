{ pkgs, python }:

self: super: {

   "cryptography" = python.overrideDerivation super."cryptography" (old: {
      buildInputs = old.buildInputs
          ++ pkgs.lib.optional pkgs.stdenv.isDarwin pkgs.darwin.apple_sdk.frameworks.Security;
   });

}
