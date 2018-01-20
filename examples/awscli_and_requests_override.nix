{ pkgs, python }:
with pkgs.lib;
let
  specificOverrides = self: super:
  {
    "awscli" = python.overrideDerivation super."awscli" (old: {
      propagatedBuildInputs = old.propagatedBuildInputs ++ [
        pkgs.groff
        pkgs.less
      ];
    });
    "jmespath" = python.overrideDerivation super."jmespath" (old: {
      postInstall = ''
        chmod +x $out/bin/jp.pyc
      '';
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
