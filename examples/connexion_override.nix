{ pkgs, python }:

self: super: {

  "jsonschema" = python.overrideDerivation super."jsonschema" (old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [self.vcversioner];
  });

}
