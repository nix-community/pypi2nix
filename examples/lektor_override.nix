{ pkgs, python }:

self: super: {

   "cryptography" = python.overrideDerivation super."cryptography" (old: {
      buildInputs = old.buildInputs
          ++ pkgs.lib.optional pkgs.stdenv.isDarwin pkgs.darwin.apple_sdk.frameworks.Security;
   });

   "watchdog" = python.overrideDerivation super."watchdog" (old: {
      buildInputs = old.buildInputs
          ++ pkgs.lib.optionals pkgs.stdenv.isDarwin 
              [ pkgs.darwin.apple_sdk.frameworks.CoreServices pkgs.darwin.cf-private ];
 
   });

}
