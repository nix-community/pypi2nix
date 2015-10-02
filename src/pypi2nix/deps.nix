{ fetchurl
, pypi_url ? "https://pypi.python.org/packages"
}:

rec {

  pipVersion = "7.1.2";
  pipHash = "3823d2343d9f3aaab21cf9c917710196";
  pipWhlHash = "5ff9fec0be479e4e36df467556deed4d";

  setuptoolsVersion = "18.3.2";
  setuptoolsHash = "d30c969065bd384266e411c446a86623";
  setuptoolsWhlHash = "58c1e15fe0c124ab0880a2691f232434";

  zcbuildoutVersion = "2.4.3";
  zcbuildoutHash = "32dcb3de0673193b78d670c29551ef6c";

  zcrecipeeggVersion = "2.0.2";
  zcrecipeeggHash = "05d50d7856092fbbb43cf737962cc987";

  buildoutRequirementsVersion = "0.2.2";
  buildoutRequirementsHash = "78104e62a71d9a8d315648a4b2574e76";

  wheelVersion = "0.26.0";
  wheelHash = "4cfc6e7e3dc7377d0164914623922a10";

  clickVersion = "5.1";
  clickHash = "9c5323008cccfe232a8b161fc8196d41";

  pipWhl = fetchurl {
    url = "${pypi_url}/py2.py3/p/pip/pip-${pipVersion}-py2.py3-none-any.whl";
    md5 = pipWhlHash;
  };

  setuptoolsWhl = fetchurl {
    url = "${pypi_url}/source/3.4/s/setuptools/setuptools-${setuptoolsVersion}-py2.py3-none-any.whl";
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

  buildoutRequirements = fetchurl {
    url = "${pypi_url}/source/b/buildout.requirements/buildout.requirements-${buildoutRequirementsVersion}.tar.gz";
    md5 = buildoutRequirementsHash;
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
