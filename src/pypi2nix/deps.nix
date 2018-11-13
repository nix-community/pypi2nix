{ fetchurl
}:

rec {

  pipVersion = "18.1";
  pipWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/c2/d7/90f34cb0d83a6c5631cf71dfe64cc1054598c843a92b400e55675cc2ac37/pip-18.1-py2.py3-none-any.whl";
    sha256 = "7909d0a0932e88ea53a7014dfd14522ffef91a464daaaf5c573343852ef98550";
  };
  pip = fetchurl {
    url = "https://files.pythonhosted.org/packages/45/ae/8a0ad77defb7cc903f09e551d88b443304a9bd6e6f124e75c0fbbf6de8f7/pip-18.1.tar.gz";
    sha256 = "c0a292bd977ef590379a3f05d7b7f65135487b67470f6281289a94e015650ea1";
  };

  setuptoolsVersion = "40.5.0";
  setuptoolsWhl = fetchurl {
    url = "https://files.pythonhosted.org/packages/82/a1/ba6fb41367b375f5cb653d1317d8ca263c636cff6566e2da1b0da716069d/setuptools-40.5.0-py2.py3-none-any.whl";
    sha256 = "e329a5c458c6acb5edc2b5c4ad44280c053ba827dc82fd5e84a83e22bb05460d";
  };

  zcbuildoutVersion = "2.12.2";
  zcbuildout = fetchurl {
    url = "https://files.pythonhosted.org/packages/d7/02/ad9b098ba8f77715ca2beb66fda9c1b674c8bcbc26e94b56ba392349fe69/zc.buildout-2.12.2.tar.gz";
    sha256 = "ff5d7e8a1361da8dfe1025d35ef6ce55e929dd8518d2a811a1cf2c948950a043";
  };

}
