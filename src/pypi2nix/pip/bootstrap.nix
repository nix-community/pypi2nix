{ stdenv, python, fetchurl, fetchgit }:

let
  _fetchSource = jsonValue:
    let cleanedJsonValue = builtins.removeAttrs jsonValue [ "__type__" ];
    in (if jsonValue."__type__" == "fetchurl" then
      fetchurl cleanedJsonValue
    else
      fetchgit cleanedJsonValue);
  wrappedPip = ''
    #!${stdenv.shell}

    exec python -m pip "$@"
  '';
  indexJson = with builtins; fromJSON (readFile ../wheels/index.json);
  packageOverrides = self: super: {
    pip = super.pip.overridePythonAttrs
      (old: { src = _fetchSource indexJson.pip; });
    setuptools = super.setuptools.overridePythonAttrs
      (old: { src = _fetchSource indexJson.setuptools; });
    wheel = super.wheel.overridePythonAttrs
      (old: { src = _fetchSource indexJson.wheel; });
  };
  overriddenPython = python.override { inherit packageOverrides; };
  pythonWithPackages =
    overriddenPython.withPackages (pkgs: with pkgs; [ pip setuptools wheel ]);
in pythonWithPackages
