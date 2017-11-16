{ fetchurl
, fetchgit
}:

rec {

  pip = {
    version = "9.0.1";
    src = fetchgit {
      url = "https://github.com/seppeljordan/pip.git";
      sha256 = "1fl1bxilnynkl7gxiz7pdd36c8abbxhm255sas5cracjg7mnkhl6";
      rev = "8ebba2cbba1fb0ecb69137f4163b3a370dead2f4";
    };
    format = "setuptools";
  };

  setuptools = {
    src = fetchgit {
      url = "https://github.com/pypa/setuptools.git";
      rev = "1b192005562d5cf0de30c02154c58fd1dca577c8";
      sha256 = "1fflgfxqcp3nazl8bsc07gj6l0786852bcr93i426wwf13kd6bfl";
    };
    format = "setuptools";
    version = "36.4.0";
  };

  six = {
    version = "1.10.0";
    format = "wheel";
    src = fetchurl {
      url = "https://pypi.python.org/packages/c8/0a/b6723e1bc4c516cb687841499455a8505b44607ab535be01091c0f24f079/six-1.10.0-py2.py3-none-any.whl";
      sha256 = "1cay6fbjmwz2lxrjbp543k1g2ivbm891mlx64njgbk4v7m08rxqg";
    };
  };

  appdirs = {
    version = "1.4.3";
    format = "wheel";
    src = fetchurl {
      url = "https://pypi.python.org/packages/56/eb/810e700ed1349edde4cbdc1b2a21e28cdf115f9faf263f6bbf8447c1abf3/appdirs-1.4.3-py2.py3-none-any.whl";
      sha256 = "0vhnw9ihh67n7n7zdsn355pflz1da1nn6m7czbfk838xarj4dcnq";
    };
  };

  packaging = {
    version = "16.8";
    src = fetchurl {
      url = "https://pypi.python.org/packages/87/1b/c39b7c65b5612812b83d6cab7ef2885eac9f6beb0b7b8a7071a186aea3b1/packaging-16.8-py2.py3-none-any.whl";
      sha256 = "1273rw8ihdbshvm95c4ih0a7rxykbh4z2s3s08r1z1d7wg36s9wr";
    };
    format = "wheel";
  };

  pyparsing = {
    version = "2.2.0";
    src = fetchurl {
      url = "https://pypi.python.org/packages/6a/8a/718fd7d3458f9fab8e67186b00abdd345b639976bc7fb3ae722e1b026a50/pyparsing-2.2.0-py2.py3-none-any.whl";
      sha256 = "046h5fmjyaainvksvmvpx70p6qack7gxcnv0s5z7w264m4bkzr7y";
    };
    format = "wheel";
  };

  zc_buildout = {
    version = "2.9.5";
    src = fetchurl {
      url = "https://github.com/buildout/buildout/archive/2.9.5.tar.gz";
      sha256 = "1xhyyqdn2sdpr5s25qnpkrizzvyc2p24n0x90jckv176dcqr2cjb";
    };
    format = "setuptools";
  };

  zc_recipe_egg = {
    version = "2.0.3";
    src = fetchurl {
      url = "https://pypi.python.org/packages/08/5e/ade683d229d77ed457017145672f1be4fd98be60f1a5344109a4e66a7d54/zc.recipe.egg-2.0.3.tar.gz";
      sha256 = "0d7xkxxhm5bwrscchjzc88559njirqxishdwl2qjx3gij3s12l5s";
    };
    format = "setuptools";
  };

  buildout_requirements = {
    version = "0.2.2";
    src = fetchurl {
      url = "https://github.com/garbas/buildout.requirements/archive/1e2977e2d254184399401746736d2b17c912b350.tar.gz";
      sha256 = "1yvyng2r55mn69n16iln5211fysz519absggn488hf5ky7xmij2q";
    };
    format = "setuptools";
  };

  wheel = {
    version = "0.30.0a0";
    src = fetchurl {
      url = "https://pypi.python.org/packages/a7/37/947b4329c4a3c72093b6c8e9b4be8c7f10c32dbb78848d3a234ce01c059d/wheel-0.30.0a0.tar.gz";
      sha256 = "1nm6mn8isny0hr86rhbfrpfj867c0phf001xgsd69xfp9ady1wwq";
    };
    format = "setuptools";
  };
}
