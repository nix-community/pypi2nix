{ fetchurl
}:

rec {

  pipVersion = "8.1.1";
  pipHash = "6b86f11841e89c8241d689956ba99ed7";
  pipWhlHash = "22db7b6a517a09c29d54a76650f170eb";

  setuptoolsVersion = "21.0.0";
  setuptoolsHash = "81964fdb89534118707742e6d1a1ddb4";
  setuptoolsWhlHash = "6027400d6870a7dad29952b7d2dfdc7b";

  zcbuildoutVersion = "2.5.1";
  zcbuildoutHash = "c88947a3c021ee1509a331c4fa9be187";

  zcrecipeeggVersion = "2.0.3";
  zcrecipeeggHash = "69a8ce276029390a36008150444aa0b4";

  wheelVersion = "0.29.0";
  wheelHash = "555a67e4507cedee23a0deb9651e452f";

  clickVersion = "6.6";
  clickHash = "d0b09582123605220ad6977175f3e51d";

  pipWhl = fetchurl {
    url = "https://pypi.python.org/packages/31/6a/0f19a7edef6c8e5065f4346137cc2a08e22e141942d66af2e1e72d851462/pip-${pipVersion}-py2.py3-none-any.whl";
    md5 = pipWhlHash;
  };

  setuptoolsWhl = fetchurl {
    url = "https://pypi.python.org/packages/15/b7/a76624e5a3b18c8c1c8d33a5240b34cdabb08aef2da44b536a8b53ba1a45/setuptools-${setuptoolsVersion}-py2.py3-none-any.whl";
    md5 = setuptoolsWhlHash;
  };

  pip = fetchurl {
    url = "https://pypi.python.org/packages/41/27/9a8d24e1b55bd8c85e4d022da2922cb206f183e2d18fee4e320c9547e751/pip-${pipVersion}.tar.gz";
    md5 = pipHash;
  };

  setuptools = fetchurl {
    url = "https://pypi.python.org/packages/ff/d4/209f4939c49e31f5524fa0027bf1c8ec3107abaf7c61fdaad704a648c281/setuptools-${setuptoolsVersion}.tar.gz";
    md5 = setuptoolsHash;
  };

  zcbuildout = fetchurl {
    url = "https://pypi.python.org/packages/bd/07/28eba9f0a9da3544611db7e1796583a9c61a3c83c26f6a80e4fd790752b1/zc.buildout-${zcbuildoutVersion}.tar.gz";
    md5 = zcbuildoutHash;
  };

  zcrecipeegg = fetchurl {
    url = "https://pypi.python.org/packages/08/5e/ade683d229d77ed457017145672f1be4fd98be60f1a5344109a4e66a7d54/zc.recipe.egg-${zcrecipeeggVersion}.tar.gz";
    md5 = zcrecipeeggHash;
  };

  wheel = fetchurl {
    url = "https://pypi.python.org/packages/c9/1d/bd19e691fd4cfe908c76c429fe6e4436c9e83583c4414b54f6c85471954a/wheel-${wheelVersion}.tar.gz";
    md5 = wheelHash;
  };

  click = fetchurl {
    url = "https://pypi.python.org/packages/7a/00/c14926d8232b36b08218067bcd5853caefb4737cda3f0a47437151344792/click-${clickVersion}.tar.gz";
    md5 = clickHash;
  };

}
