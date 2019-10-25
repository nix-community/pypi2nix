{ stdenv
, python
, fetchurl
}:

let
  wrappedPip = ''
    #!${stdenv.shell}

    exec python -m pip "$@"
  '';
  indexJson = with builtins; fromJSON (readFile ../wheels/index.json);
  packageOverrides = self: super: {
    pip = super.pip.overridePythonAttrs(old: {
      src = fetchurl indexJson.pip;
    });
    setuptools = super.setuptools.overridePythonAttrs(old: {
      src = fetchurl indexJson.setuptools;
    });
    wheel = super.wheel.overridePythonAttrs(old: {
      src = fetchurl indexJson.wheel;
    });
  };
  overriddenPython = python.override {inherit packageOverrides;};
  pythonWithPackages = overriddenPython.withPackages(pkgs: with pkgs; [pip setuptools wheel]);
in pythonWithPackages
