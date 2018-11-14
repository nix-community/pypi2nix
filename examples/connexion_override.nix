{ pkgs, python }:

self: super: {

  "connexion" = python.overrideDerivation super."connexion" (old: {
    patchPhase = ''
      sed -i \
        -e "s|jsonschema>=2.5.1,<3.0.0|jsonschema|" \
        -e "s|setup_requires=\['flake8'\],||" \
        setup.py
    '';
  });

}
