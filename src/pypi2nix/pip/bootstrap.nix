{ stdenv
, python
}:

let
  wrappedPip = ''
    #!${stdenv.shell}

    exec python -m pip "$@"
  '';
in
  stdenv.mkDerivation {
    name = "pypi2nix-bootstrap";
    buildInputs = [ python ];
    src = ../wheels;
    installPhase = ''
      PYTHONPATH=
      for wheel in $(ls $src/*.whl); do
        PYTHONPATH=$wheel:$PYTHONPATH
      done
      export PYTHONPATH
      export PIP_TARGET="$out/base"
      export PIP_NO_INDEX="true"
      export PIP_FORCE_REINSTALL="true"
      export PIP_UPGRADE="true"
      export PIP_FIND_LINKS=$src
      python -m pip install pip setuptools wheel

      mkdir -p $out/bin
      echo -e '${wrappedPip}' > $out/bin/pip

      chmod +x $out/bin/*
    '';
  }
