{ fetchurl
}:

rec {

  pipVersion = "18.0";
  pipWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/5f/25/e52d3f31441505a5f3af41213346e5b6c221c9e086a166f3703d2ddaf940/pip-18.0-py2.py3-none-any.whl";
    sha256 = "070e4bf493c7c2c9f6a08dd797dd3c066d64074c38e9e8a0fb4e6541f266d96c";
  };
  pip = fetchurl {
    url = "https://files.pythonhosted.org/packages/69/81/52b68d0a4de760a2f1979b0931ba7889202f302072cc7a0d614211bc7579/pip-18.0.tar.gz";
    sha256 = "a0e11645ee37c90b40c46d607070c4fd583e2cd46231b1c06e389c5e814eed76";
  };

  setuptoolsVersion = "40.0.0";
  setuptoolsWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/ff/f4/385715ccc461885f3cedf57a41ae3c12b5fec3f35cce4c8706b1a112a133/setuptools-40.0.0-py2.py3-none-any.whl";
    sha256 = "d68abee4eed409fbe8c302ac4d8429a1ffef912cd047a903b5701c024048dd49";
  };

  sixVersion = "1.11.0";
  sixWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl";
    sha256 = "832dc0e10feb1aa2c68dcc57dbb658f1c7e65b9b61af69048abc87a2db00a0eb";
  };

  appdirsVersion = "1.4.3";
  appdirsWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/56/eb/810e700ed1349edde4cbdc1b2a21e28cdf115f9faf263f6bbf8447c1abf3/appdirs-1.4.3-py2.py3-none-any.whl";
    sha256 = "d8b24664561d0d34ddfaec54636d502d7cea6e29c3eaf68f3df6180863e2166e";
  };

  packagingVersion = "17.1";
  packagingWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/ad/c2/b500ea05d5f9f361a562f089fc91f77ed3b4783e13a08a3daf82069b1224/packaging-17.1-py2.py3-none-any.whl";
    sha256 = "e9215d2d2535d3ae866c3d6efc77d5b24a0192cce0ff20e42896cc0664f889c0";
  };

  pyparsingVersion = "2.2.0";
  pyparsingWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/6a/8a/718fd7d3458f9fab8e67186b00abdd345b639976bc7fb3ae722e1b026a50/pyparsing-2.2.0-py2.py3-none-any.whl";
    sha256 = "fee43f17a9c4087e7ed1605bd6df994c6173c1e977d7ade7b651292fab2bd010";
  };

  zcbuildoutVersion = "2.12.1";
  zcbuildout = fetchurl {
    url = "https://files.pythonhosted.org/packages/b3/a3/5cd8f26a5ec757b803dfd3b8559371dd32736cafedbcfb5b8597bcc7e2bb/zc.buildout-2.12.1.tar.gz";
    sha256 = "1e180b62fd129a68cb3a9ec8eb0ef457e18921269a93e87ef2cc34519415332d";
  };

  zcrecipeeggVersion = "2.0.5";
  zcrecipeegg = fetchurl {
    url = "https://files.pythonhosted.org/packages/a2/a3/4f985e57b6f8bb71b334976e02bef8a2c5e630131b3e03c27d00923e34d3/zc.recipe.egg-2.0.5.tar.gz";
    sha256 = "1245ac4890123803a3f5935044795a68a6e5ca37838e2209fce450c20a9449c0";
  };

  buildoutrequirementsVersion = "0.2.2";
  buildoutrequirements = fetchurl {
    url = "https://files.pythonhosted.org/packages/c1/28/2b3103f6d8f3145f310337fd9ec286724878332020c06da34a8c2de3c71d/buildout.requirements-0.2.2.tar.gz";
    sha256 = "12612822bb24979bb65df8a420e52b6acadf5b875653b67843faed850f659bec";
  };

  wheelVersion = "0.31.1";
  wheel = fetchurl {
    url = "https://files.pythonhosted.org/packages/2a/fb/aefe5d5dbc3f4fe1e815bcdb05cbaab19744d201bbc9b59cfa06ec7fc789/wheel-0.31.1.tar.gz";
    sha256 = "0a2e54558a0628f2145d2fc822137e322412115173e8a2ddbe1c9024338ae83c";
  };

}
