{ pkgs, python }:
with pkgs.lib;
let
  specificOverrides =
    self: super: {

       "cryptography" = python.overrideDerivation super."cryptography" (old: {
          buildInputs = old.buildInputs
              ++ optional
                 pkgs.stdenv.isDarwin
                 pkgs.darwin.apple_sdk.frameworks.Security;
       });

       "watchdog" = python.overrideDerivation super."watchdog" (old: {
          buildInputs = old.buildInputs
              ++ optionals pkgs.stdenv.isDarwin
                  [ pkgs.darwin.apple_sdk.frameworks.CoreServices
                    pkgs.darwin.cf-private
                  ];

       });
    };
  commonOverrides = self: super:
    mapAttrs
    (name: drv: python.overrideDerivation super."${name}" (old: {
      postInstall =
        ( if builtins.hasAttr "postInstall" old
          then old.postInstall
          else ""
        ) + ''
          rm -f $out/bin/*.pyc # hey emacs */
        '';
    }))
    super;
in
composeExtensions commonOverrides specificOverrides
