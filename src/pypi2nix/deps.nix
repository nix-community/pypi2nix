{ fetchurl
}:

rec {

  pipVersion = "9.0.1";
  pipWhl = fetchurl {
    url = "https://pypi.python.org/packages/b6/ac/7015eb97dc749283ffdec1c3a88ddb8ae03b8fad0f0e611408f196358da3/pip-9.0.1-py2.py3-none-any.whl";
    sha256 = "1c7g5xa1yhj0bxbdynxpl9g5mcag0fzd1mc9q01w6q4418n7c2v9";
  };
  pip = fetchurl {
    url = "https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz";
    sha256 = "03clr9c1dih5n9c00c592zzvf6r1ffimywkaq9agcqdllzhl7wh9";
  };

  setuptoolsVersion = "38.5.1";
  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/43/41/033a273f9a25cb63050a390ee8397acbc7eae2159195d85f06f17e7be45a/setuptools-38.5.1-py2.py3-none-any.whl";
    sha256 = "0dga9rlrbm0vgbngwkgy1gqmlnwk3jv00d7r0k8ryhdfpwd7gzkz";
  };

  sixVersion = "1.12.0";
  sixWhl = fetchurl {
    url = "https://pypi.python.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl";
    sha256 = "1sx003ds51xwi826kbv1kddydizib2vdnmycip3a46pb1zhw0bc3";
  };

  appdirsVersion = "1.4.3";
  appdirsWhl = fetchurl {
    url = "https://pypi.python.org/packages/56/eb/810e700ed1349edde4cbdc1b2a21e28cdf115f9faf263f6bbf8447c1abf3/appdirs-1.4.3-py2.py3-none-any.whl";
    sha256 = "0vhnw9ihh67n7n7zdsn355pflz1da1nn6m7czbfk838xarj4dcnq";
  };

  packagingVersion = "16.8";
  packagingWhl = fetchurl {
    url = "https://pypi.python.org/packages/87/1b/c39b7c65b5612812b83d6cab7ef2885eac9f6beb0b7b8a7071a186aea3b1/packaging-16.8-py2.py3-none-any.whl";
    sha256 = "1273rw8ihdbshvm95c4ih0a7rxykbh4z2s3s08r1z1d7wg36s9wr";
  };

  pyparsingVersion = "2.2.0";
  pyparsingWhl = fetchurl {
    url = "https://pypi.python.org/packages/6a/8a/718fd7d3458f9fab8e67186b00abdd345b639976bc7fb3ae722e1b026a50/pyparsing-2.2.0-py2.py3-none-any.whl";
    sha256 = "046h5fmjyaainvksvmvpx70p6qack7gxcnv0s5z7w264m4bkzr7y";
  };

  zcbuildoutVersion = "2.11.0";
  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/0e/78/c473fd84c4ed95be658ab05b9819d35a699484e34c8897f9e9e53b4e96b3/zc.buildout-2.11.0.tar.gz";
    sha256 = "10pa4w5qvwzpwkwm8f262kkkhmzqf1andpmgw2gfgd2zgla0laq9";
  };

  zcrecipeeggVersion = "2.0.5";
  zcrecipeegg = fetchurl {
    url = "https://pypi.python.org/packages/a2/a3/4f985e57b6f8bb71b334976e02bef8a2c5e630131b3e03c27d00923e34d3/zc.recipe.egg-2.0.5.tar.gz";
    sha256 = "1h29jh5c4l74zh4j53l36z5fb9k8b9wl8l4kynih6f0jj14aqi8j";
  };

  buildoutrequirementsVersion = "0.2.2";
  buildoutrequirements = fetchurl {
    url = "https://github.com/garbas/buildout.requirements/archive/1e2977e2d254184399401746736d2b17c912b350.tar.gz";
    sha256 = "1yvyng2r55mn69n16iln5211fysz519absggn488hf5ky7xmij2q";
  };

  wheelVersion = "0.30.0a0";
  wheel = fetchurl {
    url = "https://pypi.python.org/packages/a7/37/947b4329c4a3c72093b6c8e9b4be8c7f10c32dbb78848d3a234ce01c059d/wheel-0.30.0a0.tar.gz";
    sha256 = "1nm6mn8isny0hr86rhbfrpfj867c0phf001xgsd69xfp9ady1wwq";
  };

}
