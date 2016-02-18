{ fetchurl
, pypi_url ? "https://pypi.python.org/packages"
}:

rec {

  pipVersion = "8.0.2";
  pipHash = "3a73c4188f8dbad6a1e6f6d44d117eeb";
  pipWhlHash = "2056f553d5b593d3a970296f229c1b79";

  setuptoolsVersion = "20.1.1";
  setuptoolsHash = "10a0f4feb9f2ea99acf634c8d7136d6d";
  setuptoolsWhlHash = "9c0765fbbe30368494ec7eb72702c67e";

  zcbuildoutVersion = "2.5.0";
  zcbuildoutHash = "4c31eb4fae176b15e1e1e7dbaba159be";

  zcrecipeeggVersion = "2.0.3";
  zcrecipeeggHash = "69a8ce276029390a36008150444aa0b4";

  wheelVersion = "0.29.0";
  wheelHash = "555a67e4507cedee23a0deb9651e452f";

  clickVersion = "6.2";
  clickHash = "83252a8095397b1f5f710fdd58b484d9";

  pipWhl = fetchurl {
    url = "${pypi_url}/py2.py3/p/pip/pip-${pipVersion}-py2.py3-none-any.whl";
    md5 = pipWhlHash;
  };

  setuptoolsWhl = fetchurl {
    url = "${pypi_url}/3.4/s/setuptools/setuptools-${setuptoolsVersion}-py2.py3-none-any.whl";
    md5 = setuptoolsWhlHash;
  };

  pip = fetchurl {
    url = "${pypi_url}/source/p/pip/pip-${pipVersion}.tar.gz";
    md5 = pipHash;
  };

  setuptools = fetchurl {
    url = "${pypi_url}/source/s/setuptools/setuptools-${setuptoolsVersion}.tar.gz";
    md5 = setuptoolsHash;
  };

  zcbuildout = fetchurl {
    url = "${pypi_url}/source/z/zc.buildout/zc.buildout-${zcbuildoutVersion}.tar.gz";
    md5 = zcbuildoutHash;
  };

  zcrecipeegg = fetchurl {
    url = "${pypi_url}/source/z/zc.recipe.egg/zc.recipe.egg-${zcrecipeeggVersion}.tar.gz";
    md5 = zcrecipeeggHash;
  };

  wheel = fetchurl {
    url = "${pypi_url}/source/w/wheel/wheel-${wheelVersion}.tar.gz";
    md5 = wheelHash;
  };

  click = fetchurl {
    url = "${pypi_url}/source/c/click/click-${clickVersion}.tar.gz";
    md5 = clickHash;
  };

}
