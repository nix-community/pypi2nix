{ pkgs, python }:

self: super: {

  "linecache2" = python.overrideDerivation super."linecache2" (old: {
    buildInputs = old.buildInputs ++ [ self."pbr" ];
    patchPhase = ''
      rm test-requirements.txt
    '';
  });

  "traceback2" = python.overrideDerivation super."traceback2" (old: {
    buildInputs = old.buildInputs ++ [ self.pbr ];
    patchPhase = ''
      rm test-requirements.txt
    '';
  });

}
