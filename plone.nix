
{ pkgs, python, buildPythonPackage }:

let plone42Packages = python.modules // rec {
  inherit python;
  inherit (pkgs) fetchurl stdenv;



  accesscontrol = buildPythonPackage rec {
    name = "accesscontrol-2.13.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/A/AccessControl/AccessControl-2.13.7.zip";
      md5 = "b64088eecdc488e6b2a5b6eced2cfaa6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  acquisition = buildPythonPackage rec {
    name = "acquisition-2.13.8";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/A/Acquisition/Acquisition-2.13.8.zip";
      md5 = "8c33160c157b50649e2b2b3224622579";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  archetypes_kss = buildPythonPackage rec {
    name = "archetypes.kss-1.7.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/a/archetypes.kss/archetypes.kss-1.7.1.zip";
      md5 = "9ce0dd5c64ed0d440d142ae5d55d6820";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  archetypes_querywidget = buildPythonPackage rec {
    name = "archetypes.querywidget-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/a/archetypes.querywidget/archetypes.querywidget-1.0.1.tar.gz";
      md5 = "310c029792694bedf6cf0c1c14981629";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_app_querystring ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  archetypes_referencebrowserwidget = buildPythonPackage rec {
    name = "archetypes.referencebrowserwidget-2.4.10";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/a/archetypes.referencebrowserwidget/archetypes.referencebrowserwidget-2.4.10.tar.gz";
      md5 = "a6056532a9ab33098762fe59834c5799";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  archetypes_schemaextender = buildPythonPackage rec {
    name = "archetypes.schemaextender-2.1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/a/archetypes.schemaextender/archetypes.schemaextender-2.1.1.zip";
      md5 = "3659dd72db341b629308d90f135031df";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  borg_localrole = buildPythonPackage rec {
    name = "borg.localrole-3.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/b/borg.localrole/borg.localrole-3.0.2.zip";
      md5 = "04082694dfda9ae5cda62747b8ac7ccf";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  collective_monkeypatcher = buildPythonPackage rec {
    name = "collective.monkeypatcher-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/c/collective.monkeypatcher/collective.monkeypatcher-1.0.1.zip";
      md5 = "4d4f20f9b8bb84b24afadc4f56f6dc2c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  collective_z3cform_datetimewidget = buildPythonPackage rec {
    name = "collective.z3cform.datetimewidget-1.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/c/collective.z3cform.datetimewidget/collective.z3cform.datetimewidget-1.0.5.tar.gz";
      md5 = "3c6703fa6ef43bc749411c90a5e1fc77";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  datetime = buildPythonPackage rec {
    name = "datetime-2.12.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/D/DateTime/DateTime-2.12.6.zip";
      md5 = "b2ade6cd7e85dd0c38c770f015c42500";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  diazo = buildPythonPackage rec {
    name = "diazo-1.0rc3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/d/diazo/diazo-1.0rc3.zip";
      md5 = "56ccfcb078e9c5a51397ccb032bd8b4e";
    };
    doCheck = false;
    propagatedBuildInputs = [ experimental_cssselect ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  documenttemplate = buildPythonPackage rec {
    name = "documenttemplate-2.13.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/D/DocumentTemplate/DocumentTemplate-2.13.2.zip";
      md5 = "07bb086c77c1dfe94125ad2efbba94b7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  docutils = buildPythonPackage rec {
    name = "docutils-0.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/d/docutils/docutils-0.7.tar.gz";
      md5 = "9aec716baf15d06b5aa57cf8d5591c15";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  elementtree = buildPythonPackage rec {
    name = "elementtree-1.2.7-20070827-preview";
    src = fetchurl {
      url = "http://effbot.org/media/downloads/elementtree-1.2.7-20070827-preview.zip";
      md5 = "30e2fe5edd143f347e03a8baf5d60f8a";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  experimental_cssselect = buildPythonPackage rec {
    name = "experimental.cssselect-0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/e/experimental.cssselect/experimental.cssselect-0.1.zip";
      md5 = "3cb5e61adee5b415784eb8db749091ee";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  extensionclass = buildPythonPackage rec {
    name = "extensionclass-2.13.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/E/ExtensionClass/ExtensionClass-2.13.2.zip";
      md5 = "0236e6d7da9e8b87b9ba45f1b8f930b8";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  feedparser = buildPythonPackage rec {
    name = "feedparser-5.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/f/feedparser/feedparser-5.0.1.tar.bz2";
      md5 = "702835de74bd4a578524f311e62c2877";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  five_customerize = buildPythonPackage rec {
    name = "five.customerize-1.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/f/five.customerize/five.customerize-1.0.2.tar.gz";
      md5 = "f3c70ff231f8443434bd4829497ad7cc";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_componentvocabulary ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  five_formlib = buildPythonPackage rec {
    name = "five.formlib-1.0.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/f/five.formlib/five.formlib-1.0.4.zip";
      md5 = "09fcecbb7e0ed4a31a4f19787c1a78b4";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  five_globalrequest = buildPythonPackage rec {
    name = "five.globalrequest-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/f/five.globalrequest/five.globalrequest-1.0.tar.gz";
      md5 = "87f8996bd21d4aa156aa26e7d21b8744";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_globalrequest ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  five_localsitemanager = buildPythonPackage rec {
    name = "five.localsitemanager-2.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/f/five.localsitemanager/five.localsitemanager-2.0.5.zip";
      md5 = "5e3a658e6068832bd802018ebc83f2d4";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  initgroups = buildPythonPackage rec {
    name = "initgroups-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/i/initgroups/initgroups-2.13.0.zip";
      md5 = "38e842dcab8445f65e701fec75213acd";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  kss_core = buildPythonPackage rec {
    name = "kss.core-1.6.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/k/kss.core/kss.core-1.6.3.zip";
      md5 = "e9e0974851499556b7d09d79e1e14f11";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_app_component zope_app_folder zope_app_pagetemplate zope_app_publication zope_app_publisher zope_datetime ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  lxml = buildPythonPackage rec {
    name = "lxml-2.3.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/l/lxml/lxml-2.3.3.tar.gz";
      md5 = "a7825793c69d004f388ec6600bad7a6f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  markdown = buildPythonPackage rec {
    name = "markdown-2.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/M/Markdown/Markdown-2.0.3.tar.gz";
      md5 = "751e8055be2433dfd1a82e0fb1b12f13";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  mechanize = buildPythonPackage rec {
    name = "mechanize-0.2.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/m/mechanize/mechanize-0.2.5.tar.gz";
      md5 = "32657f139fc2fb75bcf193b63b8c60b2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  missing = buildPythonPackage rec {
    name = "missing-2.13.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/M/Missing/Missing-2.13.1.zip";
      md5 = "9823cff54444cbbcaef8fc45d8e42572";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  multimapping = buildPythonPackage rec {
    name = "multimapping-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/M/MultiMapping/MultiMapping-2.13.0.zip";
      md5 = "d69c5904c105b9f2f085d4103e0f0586";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  persistence = buildPythonPackage rec {
    name = "persistence-2.13.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Persistence/Persistence-2.13.2.zip";
      md5 = "92693648ccdc59c8fc71f7f06b1d228c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone = buildPythonPackage rec {
    name = "plone-4.2b2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Plone/Plone-4.2b2.tar.gz";
      md5 = "d3d603d7f2a569491607c114a1dbce69";
    };
    doCheck = false;
    propagatedBuildInputs = [ pkgs.setuptools plone_app_caching plone_app_iterate plone_app_openid plone_app_theming products_cmfplacefulworkflow products_cmfplone products_kupu wicked ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_blob = buildPythonPackage rec {
    name = "plone.app.blob-1.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.blob/plone.app.blob-1.5.1.tar.gz";
      md5 = "f1b5068f00e6f6c6f38d3a48396f9475";
    };
    doCheck = false;
    propagatedBuildInputs = [ archetypes_schemaextender plone_app_imaging plone_scale ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_caching = buildPythonPackage rec {
    name = "plone.app.caching-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.caching/plone.app.caching-1.0.1.tar.gz";
      md5 = "98c07227c9c46acb5629c584a5add784";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_app_z3cform plone_cachepurging plone_caching python_dateutil z3c_form z3c_zcmlhook ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_collection = buildPythonPackage rec {
    name = "plone.app.collection-1.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.collection/plone.app.collection-1.0.2.tar.gz";
      md5 = "53bed1cd5324e28a30bee3e061a26d44";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_app_testing plone_testing unittest2 ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_content = buildPythonPackage rec {
    name = "plone.app.content-2.0.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.content/plone.app.content-2.0.7.zip";
      md5 = "b62481d0bf13c65a8913150b51ece9aa";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_contentlisting = buildPythonPackage rec {
    name = "plone.app.contentlisting-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.contentlisting/plone.app.contentlisting-1.0.1.zip";
      md5 = "14d21d806bebb17b7677fb768a5b5b93";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_uuid ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_contentmenu = buildPythonPackage rec {
    name = "plone.app.contentmenu-2.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.contentmenu/plone.app.contentmenu-2.0.5.tar.gz";
      md5 = "50de3ddf80d602ab79064d652275c2e7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_contentrules = buildPythonPackage rec {
    name = "plone.app.contentrules-2.1.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.contentrules/plone.app.contentrules-2.1.4.tar.gz";
      md5 = "539ab10403d9c0288e882f27614c6418";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_stringinterp ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_controlpanel = buildPythonPackage rec {
    name = "plone.app.controlpanel-2.2.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.controlpanel/plone.app.controlpanel-2.2.3.tar.gz";
      md5 = "a94861b89f2a1634ae43b06fa5a7f331";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_cachedescriptors ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_customerize = buildPythonPackage rec {
    name = "plone.app.customerize-1.2.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.customerize/plone.app.customerize-1.2.2.zip";
      md5 = "6a3802c4e8fbd955597adc6a8298febf";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_discussion = buildPythonPackage rec {
    name = "plone.app.discussion-2.1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.discussion/plone.app.discussion-2.1.3.tar.gz";
      md5 = "ba65a54c7771fa98a52a09e330c6d2d3";
    };
    doCheck = false;
    propagatedBuildInputs = [ collective_monkeypatcher plone_z3cform ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_folder = buildPythonPackage rec {
    name = "plone.app.folder-1.0.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.folder/plone.app.folder-1.0.4.zip";
      md5 = "90fbe9c841a2f01d06979a1869c12fce";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_form = buildPythonPackage rec {
    name = "plone.app.form-2.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.form/plone.app.form-2.0.5.tar.gz";
      md5 = "ecac76663325511a110837e7ad7c24a6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_i18n = buildPythonPackage rec {
    name = "plone.app.i18n-2.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.i18n/plone.app.i18n-2.0.1.zip";
      md5 = "39f5a8dbfe102c0309abe30a0e77f639";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_imaging = buildPythonPackage rec {
    name = "plone.app.imaging-1.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.imaging/plone.app.imaging-1.0.5.zip";
      md5 = "3b2f7597029a0f39483209ea48c52788";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_iterate = buildPythonPackage rec {
    name = "plone.app.iterate-2.1.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.iterate/plone.app.iterate-2.1.4.tar.gz";
      md5 = "e48a34f4d35ab3dc9b8a29468dd618fc";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_annotation zope_viewlet ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_jquerytools = buildPythonPackage rec {
    name = "plone.app.jquerytools-1.3.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.jquerytools/plone.app.jquerytools-1.3.1.tar.gz";
      md5 = "e7bd41f6d0bad759c5105a21f1bf48f9";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_kss = buildPythonPackage rec {
    name = "plone.app.kss-1.7.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.kss/plone.app.kss-1.7.0.zip";
      md5 = "8d50978dcc657eebed1d9383954e3ed1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_layout = buildPythonPackage rec {
    name = "plone.app.layout-2.2.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.layout/plone.app.layout-2.2.5.tar.gz";
      md5 = "3c1a92106cd41abdfd28be8bf5e43076";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_linkintegrity = buildPythonPackage rec {
    name = "plone.app.linkintegrity-1.4.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.linkintegrity/plone.app.linkintegrity-1.4.4.zip";
      md5 = "e589b02bef12ed58a01a30375f88daac";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_locales = buildPythonPackage rec {
    name = "plone.app.locales-4.0.11";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.locales/plone.app.locales-4.0.11.zip";
      md5 = "b7698515893c52df3488c883e081d887";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_openid = buildPythonPackage rec {
    name = "plone.app.openid-2.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.openid/plone.app.openid-2.0.2.tar.gz";
      md5 = "ae0748f91cab0612a498926d405d8edd";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_openid ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_portlets = buildPythonPackage rec {
    name = "plone.app.portlets-2.2.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.portlets/plone.app.portlets-2.2.3.tar.gz";
      md5 = "516854d2aa0ae78c805ad46929a6471b";
    };
    doCheck = false;
    propagatedBuildInputs = [ feedparser ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_querystring = buildPythonPackage rec {
    name = "plone.app.querystring-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.querystring/plone.app.querystring-1.0.1.tar.gz";
      md5 = "d1ac61840205b22305101736378244d3";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_redirector = buildPythonPackage rec {
    name = "plone.app.redirector-1.1.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.redirector/plone.app.redirector-1.1.2.zip";
      md5 = "fd397978aa29d0ceca425f9b08698e3d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_registry = buildPythonPackage rec {
    name = "plone.app.registry-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.registry/plone.app.registry-1.0.1.tar.gz";
      md5 = "e2bef48f39750a4c2b2afcc883b8badf";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_autoform plone_supermodel ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_search = buildPythonPackage rec {
    name = "plone.app.search-1.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.search/plone.app.search-1.0.2.tar.gz";
      md5 = "6b5c414c6adc3d82ac8ba5989e449539";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_testing = buildPythonPackage rec {
    name = "plone.app.testing-4.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.testing/plone.app.testing-4.0.2.tar.gz";
      md5 = "9e9051b434b212c83a984b3381a3b480";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_theming = buildPythonPackage rec {
    name = "plone.app.theming-1.0b8";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.theming/plone.app.theming-1.0b8.zip";
      md5 = "259a4282b25b5cbbf91c46363e522c94";
    };
    doCheck = false;
    propagatedBuildInputs = [ diazo five_globalrequest lxml plone_resource plone_subrequest plone_transformchain repoze_xmliter ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_upgrade = buildPythonPackage rec {
    name = "plone.app.upgrade-1.2b2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.upgrade/plone.app.upgrade-1.2b2.tar.gz";
      md5 = "a750ba8d21a8a831ab2f61d41d8778c5";
    };
    doCheck = false;
    propagatedBuildInputs = [ products_contentmigration products_securemailhost zope_app_cache ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_users = buildPythonPackage rec {
    name = "plone.app.users-1.1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.users/plone.app.users-1.1.3.tar.gz";
      md5 = "21b1ac5c3a8ff554f1cbf593fd1d3600";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_uuid = buildPythonPackage rec {
    name = "plone.app.uuid-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.uuid/plone.app.uuid-1.0.zip";
      md5 = "9ca8dcfb09a8a0d6bbee0f28073c3d3f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_viewletmanager = buildPythonPackage rec {
    name = "plone.app.viewletmanager-2.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.viewletmanager/plone.app.viewletmanager-2.0.2.zip";
      md5 = "2e60a9239f70ccf40bc57a58c5fc2dd7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_vocabularies = buildPythonPackage rec {
    name = "plone.app.vocabularies-2.1.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.vocabularies/plone.app.vocabularies-2.1.5.zip";
      md5 = "b747a846017387ff9f0bd201ce1be926";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_app_form ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_workflow = buildPythonPackage rec {
    name = "plone.app.workflow-2.0.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.workflow/plone.app.workflow-2.0.6.zip";
      md5 = "7e217af9bd7a9e6cd4dbe9791dd844ad";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_app_z3cform = buildPythonPackage rec {
    name = "plone.app.z3cform-0.5.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.app.z3cform/plone.app.z3cform-0.5.7.zip";
      md5 = "7a1264f686d6bce86af488129bba5c0b";
    };
    doCheck = false;
    propagatedBuildInputs = [ collective_z3cform_datetimewidget z3c_formwidget_query ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_autoform = buildPythonPackage rec {
    name = "plone.autoform-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.autoform/plone.autoform-1.0.zip";
      md5 = "b3668b52749a3ed100a61db2d17d70bb";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_browserlayer = buildPythonPackage rec {
    name = "plone.browserlayer-2.1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.browserlayer/plone.browserlayer-2.1.1.tar.gz";
      md5 = "10d5737682c3287241aab286d1477050";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_cachepurging = buildPythonPackage rec {
    name = "plone.cachepurging-1.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.cachepurging/plone.cachepurging-1.0.3.tar.gz";
      md5 = "26d47c4e2dccfb1992feb259e7e01c11";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_caching = buildPythonPackage rec {
    name = "plone.caching-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.caching/plone.caching-1.0.zip";
      md5 = "2c2e3b27d13b9101c92dfed222fde36c";
    };
    doCheck = false;
    propagatedBuildInputs = [ z3c_caching ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_contentrules = buildPythonPackage rec {
    name = "plone.contentrules-2.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.contentrules/plone.contentrules-2.0.1.zip";
      md5 = "3ae91cb7a21749e14f4cd7564dcf1619";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_fieldsets = buildPythonPackage rec {
    name = "plone.fieldsets-2.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.fieldsets/plone.fieldsets-2.0.1.zip";
      md5 = "ae0cf4288466efb440a205764e2f5280";
    };
    doCheck = false;
    propagatedBuildInputs = [ five_formlib zope_formlib ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_folder = buildPythonPackage rec {
    name = "plone.folder-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.folder/plone.folder-1.0.1.zip";
      md5 = "acb3958b623c0da35fdb259c94120396";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_i18n = buildPythonPackage rec {
    name = "plone.i18n-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.i18n/plone.i18n-2.0.zip";
      md5 = "374bc28d0c9bbd9f1b8757335c139dbf";
    };
    doCheck = false;
    propagatedBuildInputs = [ unidecode ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_indexer = buildPythonPackage rec {
    name = "plone.indexer-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.indexer/plone.indexer-1.0.zip";
      md5 = "e8bd39276902647a35721c5845ec891e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_intelligenttext = buildPythonPackage rec {
    name = "plone.intelligenttext-2.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.intelligenttext/plone.intelligenttext-2.0.1.zip";
      md5 = "bec8ed2107d3c1b63a60d49a1a88ddeb";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_keyring = buildPythonPackage rec {
    name = "plone.keyring-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.keyring/plone.keyring-2.0.zip";
      md5 = "7c450ba88c4e2b368a3279c825e4e933";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_locking = buildPythonPackage rec {
    name = "plone.locking-2.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.locking/plone.locking-2.0.3.tar.gz";
      md5 = "73b8a045121ad14e2e0ed3fc2713fa63";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_memoize = buildPythonPackage rec {
    name = "plone.memoize-1.1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.memoize/plone.memoize-1.1.1.zip";
      md5 = "d07cd14b976160e1f26a859e3370147e";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_ramcache ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_openid = buildPythonPackage rec {
    name = "plone.openid-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.openid/plone.openid-2.0.zip";
      md5 = "a7e773f6d93987f6e3d69b335dd05da2";
    };
    doCheck = false;
    propagatedBuildInputs = [ python_openid ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_outputfilters = buildPythonPackage rec {
    name = "plone.outputfilters-1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.outputfilters/plone.outputfilters-1.1.zip";
      md5 = "531bf42b242ec960691356e8514f5857";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_portlet_collection = buildPythonPackage rec {
    name = "plone.portlet.collection-2.0.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.portlet.collection/plone.portlet.collection-2.0.4.tar.gz";
      md5 = "39ba9a24e240ffe30c3a0d1984b771f1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_portlet_static = buildPythonPackage rec {
    name = "plone.portlet.static-2.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.portlet.static/plone.portlet.static-2.0.1.zip";
      md5 = "63a5f5555cd9d829e995bd7fe23a44b3";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_portlets = buildPythonPackage rec {
    name = "plone.portlets-2.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.portlets/plone.portlets-2.0.2.zip";
      md5 = "8a719cb0495081415fe03f3c8820d6b0";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_protect = buildPythonPackage rec {
    name = "plone.protect-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.protect/plone.protect-2.0.zip";
      md5 = "83c797d36c4bb8cdeefd953da7352ccc";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_keyring ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_registry = buildPythonPackage rec {
    name = "plone.registry-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.registry/plone.registry-1.0.zip";
      md5 = "ed9359f6942369b82cebcbcb3940afa2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_resource = buildPythonPackage rec {
    name = "plone.resource-1.0b6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.resource/plone.resource-1.0b6.tar.gz";
      md5 = "495d4e752eba2e5455e91760d75f7f6e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_scale = buildPythonPackage rec {
    name = "plone.scalestorage-1.2.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.scale/plone.scale-1.2.2.zip";
      md5 = "7c59522b4806ee24f5e0a5fa69c523a5";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_session = buildPythonPackage rec {
    name = "plone.session-3.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.session/plone.session-3.5.zip";
      md5 = "294910485f541affe86acf1a3da89584";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_stringinterp = buildPythonPackage rec {
    name = "plone.stringinterp-1.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.stringinterp/plone.stringinterp-1.0.5.tar.gz";
      md5 = "a60848a07b35c14639ca6aa0d9c4d66b";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_subrequest = buildPythonPackage rec {
    name = "plone.subrequest-1.6.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.subrequest/plone.subrequest-1.6.2.zip";
      md5 = "8a421a1075fbb2efb00fd76d11507111";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_supermodel = buildPythonPackage rec {
    name = "plone.supermodel-1.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.supermodel/plone.supermodel-1.0.3.zip";
      md5 = "190b0da850bf59a618b56c9fe29efe7d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_testing = buildPythonPackage rec {
    name = "plone.testingsecurity-z2-zca-zodb-4.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.testing/plone.testing-4.0.3.tar.gz";
      md5 = "33a08d9371b6eca83945b9ba90616649";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_theme = buildPythonPackage rec {
    name = "plone.theme-2.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.theme/plone.theme-2.1.zip";
      md5 = "c592d0d095e9fc76cc81597cdf6d0c37";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_transformchain = buildPythonPackage rec {
    name = "plone.transformchain-1.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.transformchain/plone.transformchain-1.0.2.tar.gz";
      md5 = "18f836f28ad78ee69ab5d182a1b7664a";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_uuid = buildPythonPackage rec {
    name = "plone.uuid-1.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.uuid/plone.uuid-1.0.2.zip";
      md5 = "498c286c250902a97f0da190e3d7b929";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plone_z3cform = buildPythonPackage rec {
    name = "plone.z3cform-0.7.8";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plone.z3cform/plone.z3cform-0.7.8.zip";
      md5 = "da891365156a5d5824d4e504465886a2";
    };
    doCheck = false;
    propagatedBuildInputs = [ z3c_batching ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plonetheme_classic = buildPythonPackage rec {
    name = "plonetheme.classic-1.2.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plonetheme.classic/plonetheme.classic-1.2.1.tar.gz";
      md5 = "a9446e60bebf806cc033489114884eae";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  plonetheme_sunburst = buildPythonPackage rec {
    name = "plonetheme.sunburst-1.2.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/plonetheme.sunburst/plonetheme.sunburst-1.2.2.tar.gz";
      md5 = "47a2e818ad40622ea2ba46ce7cf71ca2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_archetypes = buildPythonPackage rec {
    name = "products.archetypes-1.7.12";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.Archetypes/Products.Archetypes-1.7.12.tar.gz";
      md5 = "f9f18caf3dd42b14e6071a3ef4994a89";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_folder products_cmftestcase products_marshall products_validation ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_atcontenttypes = buildPythonPackage rec {
    name = "products.atcontenttypes-2.1.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ATContentTypes/Products.ATContentTypes-2.1.6.tar.gz";
      md5 = "fff448a5a85cf1f0ea6a85ac405bb629";
    };
    doCheck = false;
    propagatedBuildInputs = [ products_atreferencebrowserwidget ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_atreferencebrowserwidget = buildPythonPackage rec {
    name = "products.atreferencebrowserwidget-3.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ATReferenceBrowserWidget/Products.ATReferenceBrowserWidget-3.0.zip";
      md5 = "157bdd32155c8353450c17c649aad042";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_btreefolder2 = buildPythonPackage rec {
    name = "products.btreefolder2-2.13.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.BTreeFolder2/Products.BTreeFolder2-2.13.3.tar.gz";
      md5 = "f57c85673036af7ccd34c3fa251f6bb2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfactionicons = buildPythonPackage rec {
    name = "products.cmfactionicons-2.1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFActionIcons/Products.CMFActionIcons-2.1.3.tar.gz";
      md5 = "ab1dc62404ed11aea84dc0d782b2235e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfcalendar = buildPythonPackage rec {
    name = "products.cmfcalendar-2.2.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFCalendar/Products.CMFCalendar-2.2.2.tar.gz";
      md5 = "49458e68dc3b6826ea9a3576ac014419";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfcore = buildPythonPackage rec {
    name = "products.cmfcore-2.2.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFCore/Products.CMFCore-2.2.5.tar.gz";
      md5 = "12740b2555f1ffe94a8e39bb3357fc1e";
    };
    doCheck = false;
    propagatedBuildInputs = [ products_zsqlmethods ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfdefault = buildPythonPackage rec {
    name = "products.cmfdefault-2.2.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFDefault/Products.CMFDefault-2.2.2.tar.gz";
      md5 = "87d0a1637afb1d09731b376f72236e31";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfdifftool = buildPythonPackage rec {
    name = "products.cmfdifftool-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFDiffTool/Products.CMFDiffTool-2.0.zip";
      md5 = "7ebffea30af6b31c6a9e9dde55ac4bc1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfdynamicviewfti = buildPythonPackage rec {
    name = "products.cmfdynamicviewfti-4.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFDynamicViewFTI/Products.CMFDynamicViewFTI-4.0.2.zip";
      md5 = "d29f89c3c83b3694c6f76b8c7d9b3bb2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfeditions = buildPythonPackage rec {
    name = "products.cmfeditions-2.2.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFEditions/Products.CMFEditions-2.2.3.tar.gz";
      md5 = "256098801f2eb61b5e151bd640cfcbae";
    };
    doCheck = false;
    propagatedBuildInputs = [ products_zopeversioncontrol ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfformcontroller = buildPythonPackage rec {
    name = "products.cmfformcontroller-3.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFFormController/Products.CMFFormController-3.0.2.zip";
      md5 = "dab913bfda518714046c811e2dfe2c34";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfplacefulworkflow = buildPythonPackage rec {
    name = "products.cmfplacefulworkflow-1.5.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFPlacefulWorkflow/Products.CMFPlacefulWorkflow-1.5.6.tar.gz";
      md5 = "4ae22b4bc7aaa8ca512f0af6d4cdb2ab";
    };
    doCheck = false;
    propagatedBuildInputs = [ products_plonetestcase zope_testing ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfplone = buildPythonPackage rec {
    name = "products.cmfplone-4.2b2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFPlone/Products.CMFPlone-4.2b2.tar.gz";
      md5 = "432b3ce2e07b798732c63d08ec33a633";
    };
    doCheck = false;
    propagatedBuildInputs = [ acquisition archetypes_kss archetypes_querywidget archetypes_referencebrowserwidget borg_localrole datetime extensionclass five_customerize five_localsitemanager kss_core plone_app_blob plone_app_collection plone_app_content plone_app_contentlisting plone_app_contentmenu plone_app_contentrules plone_app_controlpanel plone_app_customerize plone_app_discussion plone_app_folder plone_app_form plone_app_i18n plone_app_jquerytools plone_app_kss plone_app_layout plone_app_linkintegrity plone_app_locales plone_app_portlets plone_app_redirector plone_app_registry plone_app_search plone_app_upgrade plone_app_users plone_app_uuid plone_app_viewletmanager plone_app_vocabularies plone_app_workflow plone_browserlayer plone_contentrules plone_fieldsets plone_i18n plone_indexer plone_intelligenttext plone_locking plone_memoize plone_portlet_collection plone_portlet_static plone_portlets plone_protect plone_registry plone_session plone_theme plonetheme_classic plonetheme_sunburst products_archetypes products_atcontenttypes products_cmfactionicons products_cmfcalendar products_cmfcore products_cmfdefault products_cmfdifftool products_cmfdynamicviewfti products_cmfeditions products_cmfformcontroller products_cmfquickinstallertool products_cmfuid products_dcworkflow products_extendedpathindex products_externaleditor products_genericsetup products_mimetypesregistry products_passwordresettool products_placelesstranslationservice products_plonelanguagetool products_plonepas products_pluggableauthservice products_pluginregistry products_portaltransforms products_resourceregistries products_statusmessages products_tinymce transaction z3c_autoinclude zodb3 zope_app_locales zope_component zope_container zope_deferredimport zope_deprecation zope_dottedname zope_event zope_i18n zope_i18nmessageid zope_interface zope_location zope_pagetemplate zope_publisher zope_site zope_structuredtext zope_tal zope_tales zope_traversing zope2 ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfquickinstallertool = buildPythonPackage rec {
    name = "products.cmfquickinstallertool-3.0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFQuickInstallerTool/Products.CMFQuickInstallerTool-3.0.5.zip";
      md5 = "fa330c70e32c291b5b1f9f7594e8af7f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmftestcase = buildPythonPackage rec {
    name = "products.cmftestcase-0.9.11";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFTestCase/Products.CMFTestCase-0.9.11.zip";
      md5 = "19ed5008a93eff36b853780dd0bca119";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_cmfuid = buildPythonPackage rec {
    name = "products.cmfuid-2.2.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.CMFUid/Products.CMFUid-2.2.1.tar.gz";
      md5 = "e20727959351dffbf0bac80613eee110";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_contentmigration = buildPythonPackage rec {
    name = "products.contentmigration-2.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.contentmigration/Products.contentmigration-2.0.3.tar.gz";
      md5 = "aeb5e7049b2e4f9404d05e751baf7342";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_dcworkflow = buildPythonPackage rec {
    name = "products.dcworkflow-2.2.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.DCWorkflow/Products.DCWorkflow-2.2.4.tar.gz";
      md5 = "c90a16c4f3611015592ba8173a5f1863";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_extendedpathindex = buildPythonPackage rec {
    name = "products.extendedpathindex-2.9";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ExtendedPathIndex/Products.ExtendedPathIndex-2.9.zip";
      md5 = "7dfd5a6c3abc87f91cbaab3798038e1f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_externaleditor = buildPythonPackage rec {
    name = "products.externaleditor-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ExternalEditor/Products.ExternalEditor-1.0.zip";
      md5 = "015350455d140233cb3aa4846cae2571";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_externalmethod = buildPythonPackage rec {
    name = "products.externalmethod-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ExternalMethod/Products.ExternalMethod-2.13.0.zip";
      md5 = "15ba953ef6cb632eb571977651252ea6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_genericsetup = buildPythonPackage rec {
    name = "products.genericsetup-1.7.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.GenericSetup/Products.GenericSetup-1.7.0.tar.gz";
      md5 = "5e72bc6f3ce9b735e22e2293415fc5f3";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_kupu = buildPythonPackage rec {
    name = "products.kupu-1.5.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.kupu/Products.kupu-1.5.0.zip";
      md5 = "0952b721f77fdb38bd0bbc0a52943cbd";
    };
    doCheck = false;
    propagatedBuildInputs = [ plone_outputfilters zope_schema ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_mailhost = buildPythonPackage rec {
    name = "products.mailhost-2.13.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.MailHost/Products.MailHost-2.13.1.zip";
      md5 = "1102e523435d8bf78a15b9ddb57478e1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_marshall = buildPythonPackage rec {
    name = "products.marshall-2.1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.Marshall/Products.Marshall-2.1.1.zip";
      md5 = "5de4b78af86ea43dc4c60314ac8f681e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_mimetools = buildPythonPackage rec {
    name = "products.mimetools-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.MIMETools/Products.MIMETools-2.13.0.zip";
      md5 = "ad5372fc1190599a19493db0864448ec";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_mimetypesregistry = buildPythonPackage rec {
    name = "products.mimetypesregistry-2.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.MimetypesRegistry/Products.MimetypesRegistry-2.0.3.zip";
      md5 = "b04aeeb9d49836272efc9ad0226d6118";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_ofsp = buildPythonPackage rec {
    name = "products.ofsp-2.13.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.OFSP/Products.OFSP-2.13.2.zip";
      md5 = "c76d40928753c2ee56db873304e65bd5";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_passwordresettool = buildPythonPackage rec {
    name = "products.passwordresettool-2.0.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PasswordResetTool/Products.PasswordResetTool-2.0.7.tar.gz";
      md5 = "81438a90361e58fc5ed6f7de26a66fb1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_placelesstranslationservice = buildPythonPackage rec {
    name = "products.placelesstranslationservice-2.0.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PlacelessTranslationService/Products.PlacelessTranslationService-2.0.3.zip";
      md5 = "a94635eb712563c5a002520713f5d6dc";
    };
    doCheck = false;
    propagatedBuildInputs = [ python_gettext ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_plonelanguagetool = buildPythonPackage rec {
    name = "products.plonelanguagetool-3.2.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PloneLanguageTool/Products.PloneLanguageTool-3.2.4.tar.gz";
      md5 = "6cdc7d49a0b76051b80ca915289ad72d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_plonepas = buildPythonPackage rec {
    name = "products.plonepas-4.0.11";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PlonePAS/Products.PlonePAS-4.0.11.tar.gz";
      md5 = "89e340fc2b7b0c236c76d4f140ed9408";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_plonetestcase = buildPythonPackage rec {
    name = "products.plonetestcase-0.9.13";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PloneTestCase/Products.PloneTestCase-0.9.13.zip";
      md5 = "be15bb96e257430de2d1b94eb1570eb4";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_pluggableauthservice = buildPythonPackage rec {
    name = "products.pluggableauthservice-1.7.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PluggableAuthService/Products.PluggableAuthService-1.7.7.tar.gz";
      md5 = "d3a2268d9c0a73dd26368c21997c009c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_pluginregistry = buildPythonPackage rec {
    name = "products.pluginregistry-1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PluginRegistry/Products.PluginRegistry-1.3.tar.gz";
      md5 = "5b166193ca1eb84dfb402051f779ebab";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_portaltransforms = buildPythonPackage rec {
    name = "products.portaltransforms-2.0.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PortalTransforms/Products.PortalTransforms-2.0.7.zip";
      md5 = "bd3568fa71e8941d049514ba91b3292e";
    };
    doCheck = false;
    propagatedBuildInputs = [ markdown ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_pythonscripts = buildPythonPackage rec {
    name = "products.pythonscripts-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.PythonScripts/Products.PythonScripts-2.13.0.zip";
      md5 = "db1fad6815cb238a58dbbab8d5e95667";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_resourceregistries = buildPythonPackage rec {
    name = "products.resourceregistries-2.0.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ResourceRegistries/Products.ResourceRegistries-2.0.6.zip";
      md5 = "36000e61b18c0b64abbf6c42b1df331b";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_securemailhost = buildPythonPackage rec {
    name = "products.securemailhost-1.1.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.SecureMailHost/Products.SecureMailHost-1.1.2.zip";
      md5 = "7db0f1fa867bd0df972082f502a7a707";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_standardcachemanagers = buildPythonPackage rec {
    name = "products.standardcachemanagers-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.StandardCacheManagers/Products.StandardCacheManagers-2.13.0.zip";
      md5 = "c5088b2b62bd26d63d9579a04369cb73";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_statusmessages = buildPythonPackage rec {
    name = "products.statusmessages-4.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.statusmessages/Products.statusmessages-4.0.zip";
      md5 = "265324b0a58a032dd0ed038103ed0473";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_tinymce = buildPythonPackage rec {
    name = "products.tinymce-1.2.10";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.TinyMCE/Products.TinyMCE-1.2.10.tar.gz";
      md5 = "04f8ae494c73bf5d7ba774c49f8e170f";
    };
    doCheck = false;
    propagatedBuildInputs = [ elementtree ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_validation = buildPythonPackage rec {
    name = "products.validation-2.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.validation/Products.validation-2.0.zip";
      md5 = "afa217e2306637d1dccbebf337caa8bf";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_zcatalog = buildPythonPackage rec {
    name = "products.zcatalog-2.13.22";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ZCatalog/Products.ZCatalog-2.13.22.zip";
      md5 = "a0463dd267982eb89b15a7389e4ea79b";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_zctextindex = buildPythonPackage rec {
    name = "products.zctextindex-2.13.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ZCTextIndex/Products.ZCTextIndex-2.13.3.zip";
      md5 = "bf95ea9fa2831237fa3c3d38fafdec96";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_zopeversioncontrol = buildPythonPackage rec {
    name = "products.zopeversioncontrol-1.1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ZopeVersionControl/Products.ZopeVersionControl-1.1.3.zip";
      md5 = "238239102f3ac798ee4f4c53343a561f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  products_zsqlmethods = buildPythonPackage rec {
    name = "products.zsqlmethods-2.13.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/P/Products.ZSQLMethods/Products.ZSQLMethods-2.13.4.zip";
      md5 = "bd1ad8fd4a9d4f8b4681401dd5b71dc1";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  python_dateutil = buildPythonPackage rec {
    name = "python-dateutil-1.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/python-dateutil/python-dateutil-1.5.tar.gz";
      md5 = "0dcb1de5e5cad69490a3b6ab63f0cfa5";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  python_gettext = buildPythonPackage rec {
    name = "python-gettext-1.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/python-gettext/python-gettext-1.2.zip";
      md5 = "cd4201d440126d1296d1d2bc2b4795f3";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  python_openid = buildPythonPackage rec {
    name = "python-openid-2.2.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/p/python-openid/python-openid-2.2.5.tar.gz";
      md5 = "393f48b162ec29c3de9e2973548ea50d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  pytz = buildPythonPackage rec {
    name = "pytz-2012c";
    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pytz/pytz-2012c.tar.gz";
      md5 = "1aa85f072e3d34ae310665967a0ce053";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  record = buildPythonPackage rec {
    name = "record-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/R/Record/Record-2.13.0.zip";
      md5 = "cfed6a89d4fb2c9cb995e9084c3071b7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  repoze_xmliter = buildPythonPackage rec {
    name = "repoze.xmliter-0.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/r/repoze.xmliter/repoze.xmliter-0.4.zip";
      md5 = "368bb3b82531f04140249c9981697953";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  restrictedpython = buildPythonPackage rec {
    name = "restrictedpython-3.6.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/R/RestrictedPython/RestrictedPython-3.6.0.zip";
      md5 = "aa75a7dcc7fbc966357837cc66cacec6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  tempstorage = buildPythonPackage rec {
    name = "tempstorage-2.12.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/t/tempstorage/tempstorage-2.12.1.zip";
      md5 = "8389f6c9a653a0ee2b82138502e28487";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  transaction = buildPythonPackage rec {
    name = "transaction-1.1.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/t/transaction/transaction-1.1.1.tar.gz";
      md5 = "30b062baa34fe1521ad979fb088c8c55";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  unidecode = buildPythonPackage rec {
    name = "unidecode-0.04.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/U/Unidecode/Unidecode-0.04.1.tar.gz";
      md5 = "c4c9ed8d40cff25c390ff5d5112b9308";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  unittest2 = buildPythonPackage rec {
    name = "unittest2-0.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/u/unittest2/unittest2-0.5.1.zip";
      md5 = "1527fb89e38343945af1166342d851ee";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  wicked = buildPythonPackage rec {
    name = "wicked-1.1.9";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/w/wicked/wicked-1.1.9.zip";
      md5 = "78ab0e6dbe28eadaae11c869d6169f69";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_lifecycleevent ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_autoinclude = buildPythonPackage rec {
    name = "z3c.autoinclude-0.3.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.autoinclude/z3c.autoinclude-0.3.4.zip";
      md5 = "6a615ae18c12b459bceb3ae28e8e7709";
    };
    doCheck = false;
    propagatedBuildInputs = [ zc_buildout ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_batching = buildPythonPackage rec {
    name = "z3c.batching-1.1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.batching/z3c.batching-1.1.0.tar.gz";
      md5 = "d1dc834781d228127ca6d15301757863";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_caching = buildPythonPackage rec {
    name = "z3c.cachingzcml-2.0a1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.caching/z3c.caching-2.0a1.tar.gz";
      md5 = "17f250b5084c2324a7d15c6810ee628e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_form = buildPythonPackage rec {
    name = "z3c.form-2.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.form/z3c.form-2.5.1.tar.gz";
      md5 = "f029f83dd226f695f55049ed1ecee95e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_formwidget_query = buildPythonPackage rec {
    name = "z3c.formwidget.query-0.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.formwidget.query/z3c.formwidget.query-0.5.tar.gz";
      md5 = "a049d9f3b11bcdc48d37379e8883c5bb";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  z3c_zcmlhook = buildPythonPackage rec {
    name = "z3c.zcmlhook-1.0b1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/z3c.zcmlhook/z3c.zcmlhook-1.0b1.tar.gz";
      md5 = "7b6c80146f5930409eb0b355ddf3daeb";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zc_buildout = buildPythonPackage rec {
    name = "zc.buildout-1.4.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zc.buildout/zc.buildout-1.4.4.tar.gz";
      md5 = "33a37eaed2f4f01801db73a4ea1496f7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zc_lockfile = buildPythonPackage rec {
    name = "zc.lockfile-1.0.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zc.lockfile/zc.lockfile-1.0.0.tar.gz";
      md5 = "6cf83766ef9935c33e240b0904c7a45e";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zconfig = buildPythonPackage rec {
    name = "zconfig-2.9.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/Z/ZConfig/ZConfig-2.9.0.zip";
      md5 = "5c932690a70c8907efd240cdd76a7bc4";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zdaemon = buildPythonPackage rec {
    name = "zdaemon-2.0.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zdaemon/zdaemon-2.0.4.tar.gz";
      md5 = "7d358297df480abe93b6565fc0213c34";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zexceptions = buildPythonPackage rec {
    name = "zexceptions-2.13.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zExceptions/zExceptions-2.13.0.zip";
      md5 = "4c679696c959040d8e656ef85ae40136";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zlog = buildPythonPackage rec {
    name = "zlog-2.11.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zLOG/zLOG-2.11.1.tar.gz";
      md5 = "68073679aaa79ac5a7b6a5c025467147";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zodb3 = buildPythonPackage rec {
    name = "zodb3test-3.10.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/Z/ZODB3/ZODB3-3.10.5.tar.gz";
      md5 = "6f180c6897a1820948fee2a6290503cd";
    };
    doCheck = false;
    propagatedBuildInputs = [ zc_lockfile ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope2 = buildPythonPackage rec {
    name = "zope2-2.13.12";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/Z/Zope2/Zope2-2.13.12.tar.gz";
      md5 = "f749aa900e580af014030eda5e4ee5ae";
    };
    doCheck = false;
    propagatedBuildInputs = [ accesscontrol documenttemplate docutils initgroups missing multimapping persistence products_btreefolder2 products_externalmethod products_mailhost products_mimetools products_ofsp products_pythonscripts products_standardcachemanagers products_zcatalog products_zctextindex pytz record restrictedpython tempstorage zconfig zdaemon zexceptions zlog zope_browser zope_browsermenu zope_browserpage zope_browserresource zope_configuration zope_contentprovider zope_contenttype zope_exceptions zope_processlifetime zope_proxy zope_ptresource zope_security zope_sendmail zope_sequencesort zope_size zope_testbrowser zopeundo ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_annotation = buildPythonPackage rec {
    name = "zope.annotation-3.5.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.annotation/zope.annotation-3.5.0.tar.gz";
      md5 = "4238153279d3f30ab5613438c8e76380";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_cache = buildPythonPackage rec {
    name = "zope.app.cache-3.7.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.cache/zope.app.cache-3.7.0.zip";
      md5 = "8dd74574e869ce236ced0de7e349bb5c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_component = buildPythonPackage rec {
    name = "zope.app.component-3.9.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.component/zope.app.component-3.9.3.tar.gz";
      md5 = "bc2dce245d2afe462529c350956711e0";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_app_container ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_container = buildPythonPackage rec {
    name = "zope.app.container-3.9.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.container/zope.app.container-3.9.1.zip";
      md5 = "e33eac9f2e2864a39a1219d415fdd231";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_copypastemove ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_content = buildPythonPackage rec {
    name = "zope.app.content-3.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.content/zope.app.content-3.5.1.tar.gz";
      md5 = "0ac6a6fcb5dd6f845759f998d8e8cbb3";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_folder = buildPythonPackage rec {
    name = "zope.app.folder-3.5.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.folder/zope.app.folder-3.5.2.tar.gz";
      md5 = "5ba3a2a7ec527a7eb0cc3c2eb7bb75e9";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_app_content ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_form = buildPythonPackage rec {
    name = "zope.app.form-4.0.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.form/zope.app.form-4.0.2.tar.gz";
      md5 = "3d2b164d9d37a71490a024aaeb412e91";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_locales = buildPythonPackage rec {
    name = "zope.app.locales-3.6.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.locales/zope.app.locales-3.6.2.tar.gz";
      md5 = "bd2b4c6040e768f33004b1210d3207fa";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_pagetemplate = buildPythonPackage rec {
    name = "zope.app.pagetemplate-3.11.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.pagetemplate/zope.app.pagetemplate-3.11.2.tar.gz";
      md5 = "2d304729c0d6a9ab67dd5ea852f19476";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_dublincore ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_publication = buildPythonPackage rec {
    name = "zope.app.publication-3.12.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.publication/zope.app.publication-3.12.0.zip";
      md5 = "d8c521287f52fb9f40fa9b8c2acb4675";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_authentication zope_error ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_app_publisher = buildPythonPackage rec {
    name = "zope.app.publisher-3.10.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.app.publisher/zope.app.publisher-3.10.2.zip";
      md5 = "66e9110e2967d8d204a65a98e2227404";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_authentication = buildPythonPackage rec {
    name = "zope.authentication-3.7.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.authentication/zope.authentication-3.7.1.zip";
      md5 = "7d6bb340610518f2fc71213cfeccda68";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_broken = buildPythonPackage rec {
    name = "zope.broken-3.6.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.broken/zope.broken-3.6.0.zip";
      md5 = "eff24d7918099a3e899ee63a9c31bee6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_browser = buildPythonPackage rec {
    name = "zope.browser-1.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.browser/zope.browser-1.3.zip";
      md5 = "4ff0ddbf64c45bfcc3189e35f4214ded";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_browsermenu = buildPythonPackage rec {
    name = "zope.browsermenu-3.9.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.browsermenu/zope.browsermenu-3.9.1.zip";
      md5 = "a47c7b1e786661c912a1150bf8d1f83f";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_browserpage = buildPythonPackage rec {
    name = "zope.browserpage-3.12.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.browserpage/zope.browserpage-3.12.2.tar.gz";
      md5 = "a543ef3cb1b42f7233b3fca23dc9ea60";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_browserresource = buildPythonPackage rec {
    name = "zope.browserresource-3.10.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.browserresource/zope.browserresource-3.10.3.zip";
      md5 = "dbfde30e82dbfa1a74c5da0cb5a4772d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_cachedescriptors = buildPythonPackage rec {
    name = "zope.cachedescriptors-3.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.cachedescriptors/zope.cachedescriptors-3.5.1.zip";
      md5 = "263459a95238fd61d17e815d97ca49ce";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_component = buildPythonPackage rec {
    name = "zope.componenthook-zcml-3.9.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.component/zope.component-3.9.5.tar.gz";
      md5 = "22780b445b1b479701c05978055d1c82";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_componentvocabulary = buildPythonPackage rec {
    name = "zope.componentvocabulary-1.0.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.componentvocabulary/zope.componentvocabulary-1.0.1.tar.gz";
      md5 = "1c8fa82ca1ab1f4b0bd2455a31fde22b";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_configuration = buildPythonPackage rec {
    name = "zope.configuration-3.7.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.configuration/zope.configuration-3.7.4.zip";
      md5 = "5b0271908ef26c05059eda76928896ea";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_container = buildPythonPackage rec {
    name = "zope.container-3.11.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.container/zope.container-3.11.2.tar.gz";
      md5 = "fc66d85a17b8ffb701091c9328983dcc";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_broken zope_filerepresentation ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_contentprovider = buildPythonPackage rec {
    name = "zope.contentprovider-3.7.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.contentprovider/zope.contentprovider-3.7.2.tar.gz";
      md5 = "1bb2132551175c0123f17939a793f812";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_contenttype = buildPythonPackage rec {
    name = "zope.contenttype-3.5.5";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.contenttype/zope.contenttype-3.5.5.zip";
      md5 = "c6ac80e6887de4108a383f349fbdf332";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_copy = buildPythonPackage rec {
    name = "zope.copy-3.5.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.copy/zope.copy-3.5.0.tar.gz";
      md5 = "a9836a5d36cd548be45210eb00407337";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_copypastemove = buildPythonPackage rec {
    name = "zope.copypastemove-3.7.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.copypastemove/zope.copypastemove-3.7.0.tar.gz";
      md5 = "f335940686d15cfc5520c42f2494a924";
    };
    doCheck = false;
    propagatedBuildInputs = [ zope_copy ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_datetime = buildPythonPackage rec {
    name = "zope.datetime-3.4.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.datetime/zope.datetime-3.4.0.tar.gz";
      md5 = "bcbaf57e8a37188acb57152899f02349";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_deferredimport = buildPythonPackage rec {
    name = "zope.deferredimport-3.5.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.deferredimport/zope.deferredimport-3.5.3.tar.gz";
      md5 = "68fce3bf4f011d4a840902fd763884ee";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_deprecation = buildPythonPackage rec {
    name = "zope.deprecation-3.4.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.deprecation/zope.deprecation-3.4.1.tar.gz";
      md5 = "8a47b0f8e1fa4e833007e5b8351bb1d4";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_dottedname = buildPythonPackage rec {
    name = "zope.dottedname-3.4.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.dottedname/zope.dottedname-3.4.6.tar.gz";
      md5 = "62d639f75b31d2d864fe5982cb23959c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_dublincore = buildPythonPackage rec {
    name = "zope.dublincore-3.7.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.dublincore/zope.dublincore-3.7.0.tar.gz";
      md5 = "2e34e42e454d896feb101ac74af62ded";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_error = buildPythonPackage rec {
    name = "zope.error-3.7.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.error/zope.error-3.7.2.tar.gz";
      md5 = "2f146bee397050d9c2be5d3971400017";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_event = buildPythonPackage rec {
    name = "zope.event-3.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.event/zope.event-3.5.1.tar.gz";
      md5 = "f18363bf9926f1762fa580cc69bd97ec";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_exceptions = buildPythonPackage rec {
    name = "zope.exceptions-3.6.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.exceptions/zope.exceptions-3.6.1.zip";
      md5 = "b735a62e1ef16e746764b4938a4d7926";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_filerepresentation = buildPythonPackage rec {
    name = "zope.filerepresentation-3.6.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.filerepresentation/zope.filerepresentation-3.6.0.tar.gz";
      md5 = "5a66212e1606597df083772fb2b1f2c6";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_formlib = buildPythonPackage rec {
    name = "zope.formlib-4.0.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.formlib/zope.formlib-4.0.6.zip";
      md5 = "eed9c94382d11a4dececd0a48ac1d3f2";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_globalrequest = buildPythonPackage rec {
    name = "zope.globalrequest-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.globalrequest/zope.globalrequest-1.0.zip";
      md5 = "ae6ff02db5ba89c1fb96ed7a73ca1cfa";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_i18n = buildPythonPackage rec {
    name = "zope.i18nzcml-3.7.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.i18n/zope.i18n-3.7.4.tar.gz";
      md5 = "a6fe9d9ad53dd7e94e87cd58fb67d3b7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_i18nmessageid = buildPythonPackage rec {
    name = "zope.i18nmessageid-3.5.3";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.i18nmessageid/zope.i18nmessageid-3.5.3.tar.gz";
      md5 = "cb84bf61c2b7353e3b7578057fbaa264";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_interface = buildPythonPackage rec {
    name = "zope.interface-3.6.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.interface/zope.interface-3.6.7.zip";
      md5 = "9df962180fbbb54eb1875cff9fe436e5";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_lifecycleevent = buildPythonPackage rec {
    name = "zope.lifecycleevent-3.6.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.lifecycleevent/zope.lifecycleevent-3.6.2.tar.gz";
      md5 = "3ba978f3ba7c0805c81c2c79ea3edb33";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_location = buildPythonPackage rec {
    name = "zope.location-3.9.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.location/zope.location-3.9.0.zip";
      md5 = "d4546ea3baf40c0ee6e217c39b351824";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_pagetemplate = buildPythonPackage rec {
    name = "zope.pagetemplate-3.5.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.pagetemplate/zope.pagetemplate-3.5.2.tar.gz";
      md5 = "caa27a15351bc2ae11f5eecb5531e6c5";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_processlifetime = buildPythonPackage rec {
    name = "zope.processlifetime-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.processlifetime/zope.processlifetime-1.0.tar.gz";
      md5 = "69604bfd668a01ebebdd616a8f26ccfe";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_proxy = buildPythonPackage rec {
    name = "zope.proxy-3.6.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.proxy/zope.proxy-3.6.1.zip";
      md5 = "a400b0a26624b17fa889dbcaa989d440";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_ptresource = buildPythonPackage rec {
    name = "zope.ptresource-3.9.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.ptresource/zope.ptresource-3.9.0.tar.gz";
      md5 = "f4645e51c15289d3fdfb4139039e18e9";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_publisher = buildPythonPackage rec {
    name = "zope.publisher-3.12.6";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.publisher/zope.publisher-3.12.6.tar.gz";
      md5 = "495131970cc7cb14de8e517fb3857ade";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_ramcache = buildPythonPackage rec {
    name = "zope.ramcache-1.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.ramcache/zope.ramcache-1.0.zip";
      md5 = "87289e15f0e51f50704adda1557c02a7";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_schema = buildPythonPackage rec {
    name = "zope.schema-3.7.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.schema/zope.schema-3.7.1.tar.gz";
      md5 = "ca6e6a3555562bbc96d69e7447b47248";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_security = buildPythonPackage rec {
    name = "zope.securityuntrustedpython-3.7.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.security/zope.security-3.7.4.tar.gz";
      md5 = "072ab8d11adc083eace11262da08630c";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_sendmail = buildPythonPackage rec {
    name = "zope.sendmail-3.7.4";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.sendmail/zope.sendmail-3.7.4.zip";
      md5 = "4ba6c32ae8c5a1b7325eb00b73902cda";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_sequencesort = buildPythonPackage rec {
    name = "zope.sequencesort-3.4.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.sequencesort/zope.sequencesort-3.4.0.tar.gz";
      md5 = "cfc35fc426a47f5c0ee43c416224b864";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_site = buildPythonPackage rec {
    name = "zope.site-3.9.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.site/zope.site-3.9.2.tar.gz";
      md5 = "36a0b8dfbd713ed452ce6973ab0a3ddb";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_size = buildPythonPackage rec {
    name = "zope.size-3.4.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.size/zope.size-3.4.1.tar.gz";
      md5 = "55d9084dfd9dcbdb5ad2191ceb5ed03d";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_structuredtext = buildPythonPackage rec {
    name = "zope.structuredtext-3.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.structuredtext/zope.structuredtext-3.5.1.tar.gz";
      md5 = "eabbfb983485d0879322bc878d2478a0";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_tal = buildPythonPackage rec {
    name = "zope.tal-3.5.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.tal/zope.tal-3.5.2.zip";
      md5 = "13869f292ba36b294736b7330b1396fd";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_tales = buildPythonPackage rec {
    name = "zope.tales-3.5.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.tales/zope.tales-3.5.1.zip";
      md5 = "be5dd9b5cd06427f3b4cdf8fc29a5b95";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_testbrowser = buildPythonPackage rec {
    name = "zope.testbrowser-3.11.1";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.testbrowser/zope.testbrowser-3.11.1.tar.gz";
      md5 = "64abbee892121e7f1a91aed12cfc155a";
    };
    doCheck = false;
    propagatedBuildInputs = [ mechanize ];
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_testing = buildPythonPackage rec {
    name = "zope.testing-3.9.7";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.testing/zope.testing-3.9.7.tar.gz";
      md5 = "8999f3d143d416dc3c8b2a5bd6f33e28";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_traversing = buildPythonPackage rec {
    name = "zope.traversing-3.13.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.traversing/zope.traversing-3.13.2.zip";
      md5 = "eaad8fc7bbef126f9f8616b074ec00aa";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zope_viewlet = buildPythonPackage rec {
    name = "zope.viewlet-3.7.2";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/z/zope.viewlet/zope.viewlet-3.7.2.tar.gz";
      md5 = "367e03096df57e2f9b74fff43f7901f9";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


  zopeundo = buildPythonPackage rec {
    name = "zopeundo-2.12.0";
    src = fetchurl {
      url = "http://a.pypi.python.org/packages/source/Z/ZopeUndo/ZopeUndo-2.12.0.zip";
      md5 = "2b8da09d1b98d5558f62e12f6e52c401";
    };
    doCheck = false;
    meta = {
        maintainers = [ stdenv.lib.maintainers.garbas ];
    };
  };


}; in plone42Packages

