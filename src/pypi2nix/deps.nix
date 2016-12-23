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

  setuptoolsVersion = "32.2.0";
  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/3a/fb/570e51a1a4b0de85eb6ec36a6c47bd5fd7a55128a1391a15b6e21d290a87/setuptools-32.2.0-py2.py3-none-any.whl";
    sha256 = "1pyszj1bzp73dj2anpr37106bimpwyj6kqgigw0gahl7dgyzk3p1";
  };

  zcbuildoutVersion = "2.5.3";
  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/e4/7b/63863f09bec5f5d7b9474209a6d4d3fc1e0bca02ecfb4c17f0cdd7b554b6/zc.buildout-${zcbuildoutVersion}.tar.gz";
    sha256 = "1ffgxw8babhf68672ah1grjn06whl0plqmgwbr6605j4qvy3lpry";
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
