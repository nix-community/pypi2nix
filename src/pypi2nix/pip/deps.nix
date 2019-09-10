{ fetchurl
}:

let
  json_index = builtins.fromJSON (builtins.readFile ../wheels/index.json);
  wheels_directory = ../wheels;
in

rec {

  pipVersion = "19.3.dev0";
  pipWhl = "${wheels_directory}/${json_index.pip}";
  pip = fetchurl {
    url = "https://files.pythonhosted.org/packages/93/ab/f86b61bef7ab14909bd7ec3cd2178feb0a1c86d451bc9bccd5a1aedcde5f/pip-19.1.1.tar.gz";
    sha256 = "44d3d7d3d30a1eb65c7e5ff1173cdf8f7467850605ac7cc3707b6064bddd0958";
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
