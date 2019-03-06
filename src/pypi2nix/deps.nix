{ fetchurl
}:

rec {

  pipVersion = "19.0.3";
  pipWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/d8/f3/413bab4ff08e1fc4828dfc59996d721917df8e8583ea85385d51125dceff/pip-19.0.3-py2.py3-none-any.whl";
    sha256 = "bd812612bbd8ba84159d9ddc0266b7fbce712fc9bc98c82dee5750546ec8ec64";
  };
  pip = fetchurl {
    url = "https://files.pythonhosted.org/packages/36/fa/51ca4d57392e2f69397cd6e5af23da2a8d37884a605f9e3f2d3bfdc48397/pip-19.0.3.tar.gz";
    sha256 = "6e6f197a1abfb45118dbb878b5c859a0edbdd33fd250100bc015b67fded4b9f2";
  };

  setuptoolsVersion = "40.8.0";
  setuptoolsWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/d1/6a/4b2fcefd2ea0868810e92d519dacac1ddc64a2e53ba9e3422c3b62b378a6/setuptools-40.8.0-py2.py3-none-any.whl";
    sha256 = "e8496c0079f3ac30052ffe69b679bd876c5265686127a3159cfa415669b7f9ab";
  };

  wheelVersion = "0.33.1";
  wheel = fetchurl {
    url = "https://files.pythonhosted.org/packages/b7/cf/1ea0f5b3ce55cacde1e84cdde6cee1ebaff51bd9a3e6c7ba4082199af6f6/wheel-0.33.1.tar.gz";
    sha256 = "178fix20jymknzx8qs6iqh6zc9rbxzd750q99dkbnxw9y9vgva36";
  };

}
