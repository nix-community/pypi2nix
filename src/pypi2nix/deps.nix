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

  setuptoolsVersion = "34.1.0";
  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/a7/62/3995dc3067cbf8d4a13ddac0f87417b9a08799c586b3faa77d62ad9085de/setuptools-34.1.0-py2.py3-none-any.whl";
    sha256 = "1fmpshqr8lfcrnn6d4njrf9qfj86vxpjwaq06g2vjf7yhabx7ngd";
  };

  sixVersion = "1.10.0";
  sixWhl = fetchurl {
    url = "https://pypi.python.org/packages/c8/0a/b6723e1bc4c516cb687841499455a8505b44607ab535be01091c0f24f079/six-1.10.0-py2.py3-none-any.whl";
    sha256 = "1cay6fbjmwz2lxrjbp543k1g2ivbm891mlx64njgbk4v7m08rxqg";
  };

  appdirsVersion = "1.4.0";
  appdirsWhl = fetchurl {
    url = "https://pypi.python.org/packages/7b/8b/eebc6e2002a1e0383f1c7108d0111d4d33ea93bf417d7e19e43ec9b87b2b/appdirs-1.4.0-py2.py3-none-any.whl";
    sha256 = "0dkpa5aynxz75ydhv2f9rlpllld5q9815h89667m6acgvdw8brc5";
  };

  packagingVersion = "16.8";
  packagingWhl = fetchurl {
    url = "https://pypi.python.org/packages/87/1b/c39b7c65b5612812b83d6cab7ef2885eac9f6beb0b7b8a7071a186aea3b1/packaging-16.8-py2.py3-none-any.whl";
    sha256 = "1273rw8ihdbshvm95c4ih0a7rxykbh4z2s3s08r1z1d7wg36s9wr";
  };

  pyparsingVersion = "2.1.10";
  pyparsingWhl = fetchurl {
    url = "https://pypi.python.org/packages/2b/f7/e5a178fc3ea4118a0edce2a8d51fc14e680c745cf4162e4285b437c43c94/pyparsing-2.1.10-py2.py3-none-any.whl";
    sha256 = "117ys98ssg9asm4gz6dav4nm7zvrw3fbac6x6cprd4p6rrx1s437";
  };

  zcbuildoutVersion = "2.6.0";
  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/7f/ce/a714ab788754373a55c1f110eff61d49ca1e7b41bcec505189fedce39794/zc.buildout-2.6.0.tar.gz";
    sha256 = "0j4bfq8x2x8gp2csykh6g9sg3mazn4fzh13qcs0qvax8sh6i66rr";
  };

  zcrecipeeggVersion = "2.0.3";
  zcrecipeegg = fetchurl {
    url = "https://pypi.python.org/packages/08/5e/ade683d229d77ed457017145672f1be4fd98be60f1a5344109a4e66a7d54/zc.recipe.egg-${zcrecipeeggVersion}.tar.gz";
    sha256 = "0d7xkxxhm5bwrscchjzc88559njirqxishdwl2qjx3gij3s12l5s";
  };

  buildoutrequirementsVersion = "0.2.2";
  buildoutrequirements = fetchurl {
    url = "https://github.com/garbas/buildout.requirements/archive/1e2977e2d254184399401746736d2b17c912b350.tar.gz";
    sha256 = "1yvyng2r55mn69n16iln5211fysz519absggn488hf5ky7xmij2q";
  };

  wheelVersion = "0.30.0a0";
  wheel = fetchurl {
    url = "https://pypi.python.org/packages/a7/37/947b4329c4a3c72093b6c8e9b4be8c7f10c32dbb78848d3a234ce01c059d/wheel-${wheelVersion}.tar.gz";
    sha256 = "1nm6mn8isny0hr86rhbfrpfj867c0phf001xgsd69xfp9ady1wwq";
  };

}
