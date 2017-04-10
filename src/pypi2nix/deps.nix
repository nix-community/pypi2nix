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

  setuptoolsVersion = "34.4.1";
  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/61/da/d37d49dc549683b7a5f1074641c6f42b4c0093dc7085bc680485ad160ef8/setuptools-34.4.1-py2.py3-none-any.whl";
    sha256 = "1l3rl0hqq5kh3cxzvwiqbs9yfxdk0n9wrmfwqmp40il4fy5sqyhz";
  };

  sixVersion = "1.10.0";
  sixWhl = fetchurl {
    url = "https://pypi.python.org/packages/c8/0a/b6723e1bc4c516cb687841499455a8505b44607ab535be01091c0f24f079/six-1.10.0-py2.py3-none-any.whl";
    sha256 = "1cay6fbjmwz2lxrjbp543k1g2ivbm891mlx64njgbk4v7m08rxqg";
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

  zcbuildoutVersion = "2.9.3";
  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/f8/bc/9784f749395bfdcb66817527cdfed111b67f8ce23997b0702cfeb8ab0e82/zc.buildout-2.9.3.tar.gz";
    sha256 = "0vrq7ccj4v828my1h5f13gr514jcj29l0wd15fkw5rp4gr4jxfn8";
  };

  zcrecipeeggVersion = "2.0.3";
  zcrecipeegg = fetchurl {
    url = "https://pypi.python.org/packages/08/5e/ade683d229d77ed457017145672f1be4fd98be60f1a5344109a4e66a7d54/zc.recipe.egg-2.0.3.tar.gz";
    sha256 = "0d7xkxxhm5bwrscchjzc88559njirqxishdwl2qjx3gij3s12l5s";
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
