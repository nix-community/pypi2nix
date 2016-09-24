{ fetchurl
}:

rec {

  pipVersion = "8.1.2";
  pipHash = "0cmpsy9lr9diskkypswm9s8glgr7w3crzh1im4zqlqv7z8zv092d";
  pipWhlHash = "18cjrd66mn4a0gwa99zzs89lrb0xn4xmajdzya6zqd7v16cdsr34";

  setuptoolsVersion = "23.0.0";
  setuptoolsWhlHash = "05iqmh70d928pnr39lv16fmcnpmgx36qdzlg4642xwrbgpfmyk83";

  zcbuildoutVersion = "2.5.2";
  zcbuildoutHash = "1v1ipa3w2blf8jyar64x8xiryzqsj5d2y92c23pnm3bg97bpyz33";

  zcrecipeeggVersion = "2.0.3";
  zcrecipeeggHash = "0d7xkxxhm5bwrscchjzc88559njirqxishdwl2qjx3gij3s12l5s";

  buildoutrequirementsVersion = "0.2.2";
  buildoutrequirementsHash = "1yvyng2r55mn69n16iln5211fysz519absggn488hf5ky7xmij2q";

  wheelVersion = "0.29.0";
  wheelHash = "0j0n38hg1jvrmyy68f9ikvzq1gs9g0sx4ws7maf8wi3bwbbqmfqy";


  # --- wheels used to bootstrap python environment ---------------------------

  pipWhl = fetchurl {
    url = "https://pypi.python.org/packages/9c/32/004ce0852e0a127f07f358b715015763273799bd798956fa930814b60f39/pip-${pipVersion}-py2.py3-none-any.whl";
    sha256 = pipWhlHash;
  };

  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/74/7c/c75c4f4032a4627406db06b742cdc7ba24c4833cd423ea7e22882380abde/setuptools-${setuptoolsVersion}-py2.py3-none-any.whl";
    sha256 = setuptoolsWhlHash;
  };


  # --- python packages needed ------------------------------------------------

  pip = fetchurl {
    url = "https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-${pipVersion}.tar.gz";
    sha256 = pipHash;
  };

  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/ec/a1/60214738d5dcb199ad97034ecf349d18f3ab69659df827a5e182585bfe48/zc.buildout-${zcbuildoutVersion}.tar.gz";
    sha256 = zcbuildoutHash;
  };

  zcrecipeegg = fetchurl {
    url = "https://pypi.python.org/packages/08/5e/ade683d229d77ed457017145672f1be4fd98be60f1a5344109a4e66a7d54/zc.recipe.egg-${zcrecipeeggVersion}.tar.gz";
    sha256 = zcrecipeeggHash;
  };

  buildoutrequirements = fetchurl {
    url = "https://github.com/garbas/buildout.requirements/archive/1e2977e2d254184399401746736d2b17c912b350.tar.gz";
    sha256 = buildoutrequirementsHash;
  };

  wheel = fetchurl {
    url = "https://pypi.python.org/packages/c9/1d/bd19e691fd4cfe908c76c429fe6e4436c9e83583c4414b54f6c85471954a/wheel-${wheelVersion}.tar.gz";
    sha256 = wheelHash;
  };

}
