{ pkgs, python }:

self: super: {

   "Lektor" = python.overrideDerivation super."Lektor" (old: {
      propagatedBuildInputs = old.propagatedBuildInputs ++ (builtins.attrValues python.modules);
   });

}
