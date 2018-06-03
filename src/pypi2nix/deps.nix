{ fetchurl
}:

rec {

  pipVersion = "10.0.1";
  pipWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/0f/74/ecd13431bcc456ed390b44c8a6e917c1820365cbebcb6a8974d1cd045ab4/pip-10.0.1-py2.py3-none-any.whl";
    sha256 = "717cdffb2833be8409433a93746744b59505f42146e8d37de6c62b430e25d6d7";
  };
  pip = fetchurl {
    url = "https://files.pythonhosted.org/packages/ae/e8/2340d46ecadb1692a1e455f13f75e596d4eab3d11a57446f08259dee8f02/pip-10.0.1.tar.gz";
    sha256 = "f2bd08e0cd1b06e10218feaf6fef299f473ba706582eb3bd9d52203fdbd7ee68";
  };

  setuptoolsVersion = "39.2.0";
  setuptoolsWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/7f/e1/820d941153923aac1d49d7fc37e17b6e73bfbd2904959fffbad77900cf92/setuptools-39.2.0-py2.py3-none-any.whl";
    sha256 = "8fca9275c89964f13da985c3656cb00ba029d7f3916b37990927ffdf264e7926";
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

  zcbuildoutVersion = "2.11.4";
  zcbuildout = fetchurl {
    url = "https://files.pythonhosted.org/packages/9c/ff/565ad4e39310910ce437656fc2eafa8a1991fda39b732afe7d6b82352aad/zc.buildout-2.11.4.tar.gz";
    sha256 = "20b22d9c99c99909b6b2dc679e8acd9e1fcf9f58e23f336d8b2c5be70617fbb2";
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
