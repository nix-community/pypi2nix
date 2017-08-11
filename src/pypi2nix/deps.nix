{ fetchurl
, fetchgit
}:

rec {

  pip = {
    version = "9.0.1";
    src = fetchgit {
      url = "https://github.com/pypa/pip.git";
      sha256 = "1zj4x89h3fypgm4czdqlr96n386ydcdlmlkyx13b5c42y3byfppd";
      rev = "d5402d33e110f0b18e628ab8cab028a0a219773c";
    };
    format = "setuptools";
  };

  setuptools = {
    src = fetchurl {
      url = "https://github.com/pypa/setuptools/archive/aa41a7a58d0e1cd0dd6715b2d4057666410114c7.tar.gz";
      sha256 = "1zqashf1sjnnrrr1aiydigd1fjhgx0yjzf8cgakqajn0gzg7q7pz";
    };
    format = "setuptools";
    version = "34.4.1";
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
    version = "2.9.3";
    src = fetchurl {
      url = "https://github.com/buildout/buildout/archive/dec1baa53fd8e9f4a4bdf98f7cd45ef2d2aee809.tar.gz";
      sha256 = "1nkw756f95a2b36z4whc8fl5hkhhn02vh08lm533i4c7b1jq1sjc";
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
