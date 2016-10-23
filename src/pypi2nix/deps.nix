{ fetchurl
}:

rec {

  pipVersion = "8.1.2";
  pipWhl = fetchurl {
    url = "https://pypi.python.org/packages/9c/32/004ce0852e0a127f07f358b715015763273799bd798956fa930814b60f39/pip-${pipVersion}-py2.py3-none-any.whl";
    sha256 = "18cjrd66mn4a0gwa99zzs89lrb0xn4xmajdzya6zqd7v16cdsr34";
  };
  pip = fetchurl {
    url = "https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-${pipVersion}.tar.gz";
    sha256 = "0cmpsy9lr9diskkypswm9s8glgr7w3crzh1im4zqlqv7z8zv092d";
  };

  setuptoolsVersion = "28.6.1";
  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/b5/9a/9ce1a45a076f977cb870bf0c9370347c9371b0e9aa9ca9859196ce58afda/setuptools-${setuptoolsVersion}.tar.gz";
    sha256 = "0187m4j0a2dgsm4pjqhm579a5lqhdnw4b7gnbjdncj63hnr67370";
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
