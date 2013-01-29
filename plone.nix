
{ pkgs, python, buildPythonPackage }:

let plone42Packages = python.modules // rec {
  inherit python;
  inherit (pkgs) fetchurl stdenv;



  accesscontrol = buildPythonPackage rec {
    name = "accesscontrol-2.13.11";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/A/AccessControl/AccessControl-2.13.11.zip";
      md5 = "7e622d99fb17914b4708d26f245cb696";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime extensionclass persistence record restrictedpython transaction zexceptions zodb3 zope_component zope_configuration zope_deferredimport zope_interface zope_publisher zope_schema zope_security zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  acquisition = buildPythonPackage rec {
    name = "acquisition-2.13.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/A/Acquisition/Acquisition-2.13.8.zip";
      md5 = "8c33160c157b50649e2b2b3224622579";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  archetypes_kss = buildPythonPackage rec {
    name = "archetypes.kss-1.7.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/a/archetypes.kss/${name}.zip";
      md5 = "a8502140123b74f1b7ed4f36d3e56ff3";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_uuid setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  archetypes_querywidget = buildPythonPackage rec {
    name = "archetypes.querywidget-1.0.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/a/archetypes.querywidget/${name}.zip";
      md5 = "cbe134f2806191fd35066bbb7c85bfcc";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_app_jquerytools plone_app_querystring setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  archetypes_referencebrowserwidget = buildPythonPackage rec {
    name = "archetypes.referencebrowserwidget-2.4.16";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/a/archetypes.referencebrowserwidget/${name}.zip";
      md5 = "7dd3b0d4e188828701a291449c7495f4";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_app_form plone_app_jquerytools setuptools zope_component zope_formlib zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  archetypes_schemaextender = buildPythonPackage rec {
    name = "archetypes.schemaextender-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/a/archetypes.schemaextender/${name}.zip";
      md5 = "865aa5b4b6b26e3bb650d89ddfe77c87";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_uuid setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  borg_localrole = buildPythonPackage rec {
    name = "borg.localrole-3.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/b/borg.localrole/${name}.zip";
      md5 = "04082694dfda9ae5cda62747b8ac7ccf";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition plone_memoize products_cmfcore products_genericsetup products_plonepas products_pluggableauthservice setuptools zope_annotation zope_component zope_deferredimport zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  collective_monkeypatcher = buildPythonPackage rec {
    name = "collective.monkeypatcher-1.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/c/collective.monkeypatcher/${name}.zip";
      md5 = "4d4f20f9b8bb84b24afadc4f56f6dc2c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  collective_z3cform_datetimewidget = buildPythonPackage rec {
    name = "collective.z3cform.datetimewidget-1.2.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/c/collective.z3cform.datetimewidget/${name}.zip";
      md5 = "89daf27c7f0f235f9c001f0ee50d76e5";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools z3c_form zope_deprecation zope_i18n ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  datetime = buildPythonPackage rec {
    name = "datetime-2.12.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/D/DateTime/DateTime-2.12.7.zip";
      md5 = "72a8bcf80b52211ae7fdfe36c693d70c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ pytz zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  diazo = buildPythonPackage rec {
    name = "diazo-1.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/diazo/${name}.zip";
      md5 = "d3c2b017af521db4c86fb360c86e0bc8";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ experimental_cssselect lxml setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  documenttemplate = buildPythonPackage rec {
    name = "documenttemplate-2.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/D/DocumentTemplate/DocumentTemplate-2.13.2.zip";
      md5 = "07bb086c77c1dfe94125ad2efbba94b7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ accesscontrol acquisition extensionclass restrictedpython zexceptions zope_sequencesort zope_structuredtext ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  docutils = buildPythonPackage rec {
    name = "docutils-0.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/d/docutils/${name}.1.tar.gz";
      md5 = "b0d5cd5298fedf9c62f5fd364a274d56";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  elementtree = buildPythonPackage rec {
    name = "elementtree-1.2.7-20070827-preview";

    src = fetchurl {
      url = "http://effbot.org/media/downloads/elementtree-1.2.7-20070827-preview.zip";
      md5 = "30e2fe5edd143f347e03a8baf5d60f8a";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  experimental_cssselect = buildPythonPackage rec {
    name = "experimental.cssselect-0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/e/experimental.cssselect/${name}.zip";
      md5 = "3fecdcf1fbc3ea6025e115a56a262957";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ lxml setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  extensionclass = buildPythonPackage rec {
    name = "extensionclass-2.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/E/ExtensionClass/ExtensionClass-2.13.2.zip";
      md5 = "0236e6d7da9e8b87b9ba45f1b8f930b8";
    };

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  feedparser = buildPythonPackage rec {
    name = "feedparser-5.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/f/feedparser/${name}.tar.bz2";
      md5 = "702835de74bd4a578524f311e62c2877";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  five_customerize = buildPythonPackage rec {
    name = "five.customerize-1.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/f/five.customerize/${name}.zip";
      md5 = "32f597c2fa961f7dcc84b23e655d928e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition plone_portlets setuptools transaction zope_app_pagetemplate zope_component zope_componentvocabulary zope_dottedname zope_interface zope_lifecycleevent zope_pagetemplate zope_publisher zope_schema zope_site zope_testing zope_traversing zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  five_formlib = buildPythonPackage rec {
    name = "five.formlib-1.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/f/five.formlib/${name}.zip";
      md5 = "09fcecbb7e0ed4a31a4f19787c1a78b4";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass setuptools transaction zope_app_form zope_browser zope_component zope_event zope_formlib zope_i18nmessageid zope_interface zope_lifecycleevent zope_location zope_publisher zope_schema zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  five_globalrequest = buildPythonPackage rec {
    name = "five.globalrequest-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/f/five.globalrequest/${name}.tar.gz";
      md5 = "87f8996bd21d4aa156aa26e7d21b8744";
    };

    propagatedBuildInputs = [ setuptools zope_globalrequest zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  five_localsitemanager = buildPythonPackage rec {
    name = "five.localsitemanager-2.0.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/f/five.localsitemanager/${name}.zip";
      md5 = "5e3a658e6068832bd802018ebc83f2d4";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition setuptools zodb3 zope_component zope_event zope_interface zope_lifecycleevent zope_location zope_site zope_testing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  initgroups = buildPythonPackage rec {
    name = "initgroups-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/i/initgroups/${name}.zip";
      md5 = "38e842dcab8445f65e701fec75213acd";
    };

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  kss_core = buildPythonPackage rec {
    name = "kss.core-1.6.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/k/kss.core/${name}.zip";
      md5 = "87e66e78c3bbd7af3ecce5b2fef935ae";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_browserpage zope_browserresource zope_component zope_configuration zope_contenttype zope_datetime zope_event zope_interface zope_lifecycleevent zope_location zope_pagetemplate zope_publisher zope_schema zope_security zope_site zope_testing zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  lxml = buildPythonPackage rec {
    name = "lxml-3.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/l/lxml/${name}.tar.gz";
      md5 = "38b15b0dd5e9292cf98be800e84a3ce4";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  markdown = buildPythonPackage rec {
    name = "markdown-2.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.3.tar.gz";
      md5 = "751e8055be2433dfd1a82e0fb1b12f13";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  mechanize = buildPythonPackage rec {
    name = "mechanize-0.2.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/m/mechanize/${name}.tar.gz";
      md5 = "32657f139fc2fb75bcf193b63b8c60b2";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  missing = buildPythonPackage rec {
    name = "missing-2.13.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/M/Missing/Missing-2.13.1.zip";
      md5 = "9823cff54444cbbcaef8fc45d8e42572";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  multimapping = buildPythonPackage rec {
    name = "multimapping-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/M/MultiMapping/MultiMapping-2.13.0.zip";
      md5 = "d69c5904c105b9f2f085d4103e0f0586";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  persistence = buildPythonPackage rec {
    name = "persistence-2.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Persistence/Persistence-2.13.2.zip";
      md5 = "92693648ccdc59c8fc71f7f06b1d228c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass zodb3 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone = buildPythonPackage rec {
    name = "plone-4.2.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Plone/Plone-4.2.4.zip";
      md5 = "688438bd541e7cb2ab650c8c59282b85";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_blob = buildPythonPackage rec {
    name = "plone.app.blob-1.5.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.blob/${name}.zip";
      md5 = "8d6ba6f360b6bfd40f87914132339660";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ archetypes_schemaextender plone_app_imaging plone_scale setuptools zodb3 zope_proxy ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_caching = buildPythonPackage rec {
    name = "plone.app.caching-1.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.caching/${name}.zip";
      md5 = "83a52efeb7604d4c5b4afbc6c1365c6f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition plone_app_registry plone_app_z3cform plone_cachepurging plone_caching plone_memoize plone_protect plone_registry products_cmfcore products_cmfdynamicviewfti products_genericsetup products_statusmessages python_dateutil setuptools z3c_form z3c_zcmlhook zope_browserresource zope_component zope_interface zope_pagetemplate zope_publisher zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_collection = buildPythonPackage rec {
    name = "plone.app.collection-1.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.collection/${name}.zip";
      md5 = "40c9035472e386fc9d0ec1b9a9a3d4f6";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_content = buildPythonPackage rec {
    name = "plone.app.content-2.0.12";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.content/${name}.zip";
      md5 = "2f14a85fb66d73e0b699b839caaaad26";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_contentlisting = buildPythonPackage rec {
    name = "plone.app.contentlisting-1.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.contentlisting/${name}.zip";
      md5 = "fa6eb45c4ffd0eb3817ad4813ca24916";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_uuid setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_contentmenu = buildPythonPackage rec {
    name = "plone.app.contentmenu-2.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.contentmenu/${name}.zip";
      md5 = "b1c7e5a37c659ba30b3a077e149b1752";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_contentrules = buildPythonPackage rec {
    name = "plone.app.contentrules-2.1.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.contentrules/${name}.zip";
      md5 = "74d2fed9095a7c5f890b6f27de78dafc";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_controlpanel = buildPythonPackage rec {
    name = "plone.app.controlpanel-2.2.11";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.controlpanel/${name}.zip";
      md5 = "401c8880865f398c281953f5837108b9";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_customerize = buildPythonPackage rec {
    name = "plone.app.customerize-1.2.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.customerize/${name}.zip";
      md5 = "6a3802c4e8fbd955597adc6a8298febf";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition five_customerize plone_browserlayer plone_portlets products_cmfcore setuptools zope_component zope_interface zope_publisher zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_discussion = buildPythonPackage rec {
    name = "plone.app.discussion-2.1.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.discussion/${name}.zip";
      md5 = "b0cb1fbdf8a7a238cf5a58fb10c24731";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_folder = buildPythonPackage rec {
    name = "plone.app.folder-1.0.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.folder/${name}.zip";
      md5 = "8ea860daddb4c93c0b7f2b5f7106fef0";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_form = buildPythonPackage rec {
    name = "plone.app.form-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.form/${name}.zip";
      md5 = "8017f8f782d992825ed71d16b126c4e7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime five_formlib plone_app_vocabularies plone_locking products_cmfcore products_cmfdefault setuptools zope_browser zope_component zope_event zope_formlib zope_i18n zope_i18nmessageid zope_interface zope_lifecycleevent zope_schema zope_site zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_i18n = buildPythonPackage rec {
    name = "plone.app.i18n-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.i18n/${name}.zip";
      md5 = "a10026573463dfc1899bf4062cebdbf2";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_imaging = buildPythonPackage rec {
    name = "plone.app.imaging-1.0.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.imaging/${name}.zip";
      md5 = "8d494cd69b3f6be7fcb9e21c20277765";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_scale setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_iterate = buildPythonPackage rec {
    name = "plone.app.iterate-2.1.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.iterate/${name}.zip";
      md5 = "db598cfc0986737145ddc7e6b70a1794";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime plone_locking plone_memoize products_archetypes products_cmfcore products_cmfeditions products_cmfplacefulworkflow products_dcworkflow products_statusmessages setuptools zodb3 zope_annotation zope_component zope_event zope_i18nmessageid zope_interface zope_lifecycleevent zope_schema zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_jquery = buildPythonPackage rec {
    name = "plone.app.jquery-1.4.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.jquery/${name}.zip";
      md5 = "a12d56f3dfd2ba6840bf21a6bd860b90";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_jquerytools = buildPythonPackage rec {
    name = "plone.app.jquerytools-1.3.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.jquerytools/${name}.zip";
      md5 = "326470a34e07aa98c40d75ec22484572";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools zope_component zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_kss = buildPythonPackage rec {
    name = "plone.app.kss-1.7.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.kss/${name}.zip";
      md5 = "97a35086fecfe25e55b65042eb35e796";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_layout = buildPythonPackage rec {
    name = "plone.app.layout-2.2.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.layout/${name}.zip";
      md5 = "90ea408f5e01aeb01517d55eb6b6063a";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_linkintegrity = buildPythonPackage rec {
    name = "plone.app.linkintegrity-1.5.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.linkintegrity/${name}.zip";
      md5 = "41810cc85ca05921a329aac5bc4cf403";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_locales = buildPythonPackage rec {
    name = "plone.app.locales-4.2.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.locales/${name}.zip";
      md5 = "baf48a0a5278a18fa1c2848d3470464f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_openid = buildPythonPackage rec {
    name = "plone.app.openid-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.openid/${name}.tar.gz";
      md5 = "ae0748f91cab0612a498926d405d8edd";
    };

    propagatedBuildInputs = [ plone_app_portlets plone_openid plone_portlets products_cmfcore products_plonepas products_pluggableauthservice setuptools zope_component zope_i18nmessageid zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_portlets = buildPythonPackage rec {
    name = "plone.app.portlets-2.3.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.portlets/${name}.zip";
      md5 = "534be67a7a17a71ca1e76f6f149ff2ac";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_querystring = buildPythonPackage rec {
    name = "plone.app.querystring-1.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.querystring/${name}.zip";
      md5 = "b501910b23def9b58e8309d1e469eb6f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ datetime plone_app_contentlisting plone_app_layout plone_app_registry plone_app_vocabularies plone_registry products_cmfcore products_cmfplone setuptools zope_component zope_dottedname zope_globalrequest zope_i18n zope_i18nmessageid zope_interface zope_publisher zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_redirector = buildPythonPackage rec {
    name = "plone.app.redirector-1.1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.redirector/${name}.zip";
      md5 = "7d441340a83b8ed72a03bc16148a5f21";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_memoize setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_registry = buildPythonPackage rec {
    name = "plone.app.registry-1.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.registry/${name}.zip";
      md5 = "0fdbb01e9ff71108f1be262c39b41b81";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_search = buildPythonPackage rec {
    name = "plone.app.search-1.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.search/${name}.zip";
      md5 = "bd5a1f4b5016a6d0a8697e7a9cc04833";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_app_contentlisting setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_theming = buildPythonPackage rec {
    name = "plone.app.theming-1.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.theming/${name}.zip";
      md5 = "2da6d810e0d5f295dd0daa2b60731a1b";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ diazo five_globalrequest lxml plone_app_registry plone_resource plone_subrequest plone_transformchain products_cmfplone repoze_xmliter setuptools zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_upgrade = buildPythonPackage rec {
    name = "plone.app.upgrade-1.2.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.upgrade/${name}.zip";
      md5 = "2798dd50863d8c25624400b988a0acdd";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_users = buildPythonPackage rec {
    name = "plone.app.users-1.1.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.users/${name}.zip";
      md5 = "97895d8dbdf885784be1afbf5b8b364c";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_uuid = buildPythonPackage rec {
    name = "plone.app.uuid-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.uuid/${name}.zip";
      md5 = "9ca8dcfb09a8a0d6bbee0f28073c3d3f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_indexer plone_uuid setuptools zope_interface zope_publisher ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_viewletmanager = buildPythonPackage rec {
    name = "plone.app.viewletmanager-2.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.viewletmanager/${name}.zip";
      md5 = "1dbc51c7664ce3e6ca4dcca1b7b86082";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition plone_app_vocabularies products_genericsetup setuptools zodb3 zope_component zope_contentprovider zope_interface zope_site zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_vocabularies = buildPythonPackage rec {
    name = "plone.app.vocabularies-2.1.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.vocabularies/${name}.zip";
      md5 = "34d4eb9c95879811fec0875aa3235ed3";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_cmfcore setuptools zope_browser zope_component zope_formlib zope_i18n zope_i18nmessageid zope_interface zope_schema zope_site zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_workflow = buildPythonPackage rec {
    name = "plone.app.workflow-2.0.10";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.workflow/${name}.zip";
      md5 = "350ea680ccf7eb9b1598927cafad4f38";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_app_z3cform = buildPythonPackage rec {
    name = "plone.app.z3cform-0.6.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.app.z3cform/${name}.zip";
      md5 = "2e77f5e03d48a6fb2eb9994edb871917";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ collective_z3cform_datetimewidget kss_core plone_app_kss plone_z3cform setuptools z3c_formwidget_query zope_browserpage zope_component zope_interface zope_traversing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_autoform = buildPythonPackage rec {
    name = "plone.autoform-1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.autoform/${name}.zip";
      md5 = "4cb2935ba9cda3eb3ee801ad8cda7c60";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_supermodel plone_z3cform setuptools z3c_form zope_dottedname zope_interface zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_browserlayer = buildPythonPackage rec {
    name = "plone.browserlayer-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.browserlayer/${name}.zip";
      md5 = "bce02f4907a4f29314090c525e5fc28e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools zope_component zope_interface zope_traversing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_cachepurging = buildPythonPackage rec {
    name = "plone.cachepurging-1.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.cachepurging/${name}.zip";
      md5 = "886814ac4deef0f1ed99a2eb60864264";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ five_globalrequest plone_registry setuptools zope_annotation zope_component zope_event zope_i18nmessageid zope_interface zope_lifecycleevent zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_caching = buildPythonPackage rec {
    name = "plone.caching-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.caching/${name}.zip";
      md5 = "2c2e3b27d13b9101c92dfed222fde36c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ five_globalrequest plone_registry plone_transformchain setuptools z3c_caching zope_component zope_i18nmessageid zope_interface zope_schema zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_contentrules = buildPythonPackage rec {
    name = "plone.contentrules-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.contentrules/${name}.zip";
      md5 = "a32370656c4fd58652fcd8a234db69c5";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_annotation zope_component zope_componentvocabulary zope_configuration zope_container zope_i18nmessageid zope_interface zope_lifecycleevent zope_schema zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_fieldsets = buildPythonPackage rec {
    name = "plone.fieldsets-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.fieldsets/${name}.zip";
      md5 = "4158c8a1f784fcb5cecbd63deda7222f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ five_formlib setuptools zope_component zope_formlib zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_folder = buildPythonPackage rec {
    name = "plone.folder-1.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.folder/${name}.zip";
      md5 = "1674ff18b7a9452d0c2063cf11c679b7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_memoize setuptools zope_annotation zope_component zope_container zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_i18n = buildPythonPackage rec {
    name = "plone.i18n-2.0.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.i18n/${name}.zip";
      md5 = "ef36aa9a294d507abb37787f9f7700bd";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools unidecode zope_component zope_i18n zope_interface zope_publisher ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_indexer = buildPythonPackage rec {
    name = "plone.indexer-1.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.indexer/${name}.zip";
      md5 = "538aeee1f9db78bc8c85ae1bcb0153ed";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore setuptools zope_component zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_intelligenttext = buildPythonPackage rec {
    name = "plone.intelligenttext-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.intelligenttext/${name}.zip";
      md5 = "51688fa0815b49e00334e3ef948328ba";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_keyring = buildPythonPackage rec {
    name = "plone.keyring-2.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.keyring/${name}.zip";
      md5 = "f3970e9bddb2cc65e461a2c62879233f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_container zope_interface zope_location ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_locking = buildPythonPackage rec {
    name = "plone.locking-2.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.locking/${name}.zip";
      md5 = "a7f8b8db78f57272d351d7fe0d067eb2";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime products_cmfcore setuptools zodb3 zope_annotation zope_component zope_i18nmessageid zope_interface zope_schema zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_memoize = buildPythonPackage rec {
    name = "plone.memoize-1.1.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.memoize/${name}.zip";
      md5 = "d07cd14b976160e1f26a859e3370147e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_annotation zope_component zope_interface zope_ramcache ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_openid = buildPythonPackage rec {
    name = "plone.openid-2.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.openid/${name}.zip";
      md5 = "d4c36926a6dbefed035ed92c29329ce1";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_pluggableauthservice python_openid setuptools transaction zodb3 zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_outputfilters = buildPythonPackage rec {
    name = "plone.outputfilters-1.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.outputfilters/${name}.zip";
      md5 = "a5ef28580f7fa7f2dc1768893995b0f7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_genericsetup products_mimetypesregistry products_portaltransforms setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_portlet_collection = buildPythonPackage rec {
    name = "plone.portlet.collection-2.1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.portlet.collection/${name}.zip";
      md5 = "5f0006dbb3e0b56870383dfdedc49228";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_app_form plone_app_portlets plone_app_vocabularies plone_memoize plone_portlets setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_portlet_static = buildPythonPackage rec {
    name = "plone.portlet.static-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.portlet.static/${name}.zip";
      md5 = "ec0dc691b4191a41ff97779b117f9985";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_app_form plone_app_portlets plone_i18n plone_portlets setuptools zope_component zope_formlib zope_i18nmessageid zope_interface zope_schema zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_portlets = buildPythonPackage rec {
    name = "plone.portlets-2.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.portlets/${name}.zip";
      md5 = "12b9a33f787756a48617c2d2dd63c538";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_memoize setuptools zodb3 zope_annotation zope_component zope_container zope_contentprovider zope_interface zope_publisher zope_schema zope_site ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_protect = buildPythonPackage rec {
    name = "plone.protect-2.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.protect/${name}.zip";
      md5 = "74925ffb08782e72f9b1e850fa78fffa";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_keyring setuptools zope_component zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_registry = buildPythonPackage rec {
    name = "plone.registry-1.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.registry/${name}.zip";
      md5 = "6be3d2ec7e2d170e29b8c0bc65049aff";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_component zope_dottedname zope_event zope_interface zope_schema zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_resource = buildPythonPackage rec {
    name = "plone.resource-1.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.resource/${name}.zip";
      md5 = "594d41e3acd913ae92f2e9ef96503b9f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_caching python_dateutil setuptools z3c_caching zope_component zope_configuration zope_filerepresentation zope_interface zope_publisher zope_schema zope_traversing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_scale = buildPythonPackage rec {
    name = "plone.scalestorage-1.2.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.scale/plone.scale-1.2.2.zip";
      md5 = "7c59522b4806ee24f5e0a5fa69c523a5";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools persistence zope_annotation zope_component zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_session = buildPythonPackage rec {
    name = "plone.session-3.5.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.session/${name}.zip";
      md5 = "2f9d3b88e813a47135af56a4da8bbde1";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_keyring plone_protect products_pluggableauthservice setuptools zope_component zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_stringinterp = buildPythonPackage rec {
    name = "plone.stringinterp-1.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.stringinterp/${name}.zip";
      md5 = "81909716210c6ac3fd0ee87f45ea523d";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore setuptools zope_i18n ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_subrequest = buildPythonPackage rec {
    name = "plone.subrequest-1.6.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.subrequest/${name}.zip";
      md5 = "cc12f68a22565415b10dbeef0020baa4";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ five_globalrequest setuptools zope_globalrequest ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_supermodel = buildPythonPackage rec {
    name = "plone.supermodel-1.1.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.supermodel/${name}.zip";
      md5 = "00b3d723bb1a48116fe3bf8754f17085";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ elementtree setuptools z3c_zcmlhook zope_component zope_deferredimport zope_dottedname zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_theme = buildPythonPackage rec {
    name = "plone.theme-2.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.theme/${name}.zip";
      md5 = "c592d0d095e9fc76cc81597cdf6d0c37";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_cmfdefault setuptools zope_component zope_interface zope_publisher zope_traversing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_transformchain = buildPythonPackage rec {
    name = "plone.transformchain-1.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.transformchain/${name}.zip";
      md5 = "f5fb7ca894249e3e666501c4fae52a6c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_component zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_uuid = buildPythonPackage rec {
    name = "plone.uuid-1.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.uuid/${name}.zip";
      md5 = "183fe2911a7d6c9f6b3103855e98ad8a";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_browserpage zope_interface zope_lifecycleevent zope_publisher ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plone_z3cform = buildPythonPackage rec {
    name = "plone.z3cform-0.7.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plone.z3cform/${name}.zip";
      md5 = "da891365156a5d5824d4e504465886a2";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ collective_monkeypatcher setuptools z3c_batching z3c_form zope_component zope_i18n ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plonetheme_classic = buildPythonPackage rec {
    name = "plonetheme.classic-1.2.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plonetheme.classic/${name}.zip";
      md5 = "9dc15871937f9cdf94cdfdb9be77a221";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  plonetheme_sunburst = buildPythonPackage rec {
    name = "plonetheme.sunburst-1.2.8";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/plonetheme.sunburst/${name}.zip";
      md5 = "be02660c869e04ac8cf6ade3559f2516";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_archetypes = buildPythonPackage rec {
    name = "products.archetypes-1.8.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.Archetypes/Products.Archetypes-1.8.6.zip";
      md5 = "74be68879b27228c084a9be869132a98";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_atcontenttypes = buildPythonPackage rec {
    name = "products.atcontenttypes-2.1.11";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ATContentTypes/Products.ATContentTypes-2.1.11.zip";
      md5 = "abfb5209ffa11dc2c1a15c488e75d89c";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_atreferencebrowserwidget = buildPythonPackage rec {
    name = "products.atreferencebrowserwidget-3.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ATReferenceBrowserWidget/Products.ATReferenceBrowserWidget-3.0.zip";
      md5 = "157bdd32155c8353450c17c649aad042";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ archetypes_referencebrowserwidget setuptools zope_deprecation ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_btreefolder2 = buildPythonPackage rec {
    name = "products.btreefolder2-2.13.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.BTreeFolder2/Products.BTreeFolder2-2.13.3.tar.gz";
      md5 = "f57c85673036af7ccd34c3fa251f6bb2";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfactionicons = buildPythonPackage rec {
    name = "products.cmfactionicons-2.1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFActionIcons/Products.CMFActionIcons-2.1.3.tar.gz";
      md5 = "ab1dc62404ed11aea84dc0d782b2235e";
    };

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfcalendar = buildPythonPackage rec {
    name = "products.cmfcalendar-2.2.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFCalendar/Products.CMFCalendar-2.2.2.tar.gz";
      md5 = "49458e68dc3b6826ea9a3576ac014419";
    };

    propagatedBuildInputs = [ products_cmfcore products_cmfdefault products_genericsetup setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfcore = buildPythonPackage rec {
    name = "products.cmfcore-2.2.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFCore/Products.CMFCore-2.2.7.tar.gz";
      md5 = "9320a4023b8575097feacfd4a400e930";
    };

    propagatedBuildInputs = [ five_localsitemanager products_genericsetup products_zsqlmethods setuptools zope_app_publication zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfdefault = buildPythonPackage rec {
    name = "products.cmfdefault-2.2.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFDefault/Products.CMFDefault-2.2.3.tar.gz";
      md5 = "fe7d2d3906ee0e3b484e4a02401576ab";
    };

    propagatedBuildInputs = [ five_formlib products_cmfcore products_genericsetup setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfdifftool = buildPythonPackage rec {
    name = "products.cmfdifftool-2.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFDiffTool/Products.CMFDiffTool-2.0.1.zip";
      md5 = "7b7ed9b8f7b4f438e92e299823f92c86";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_cmfcore products_genericsetup setuptools zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfdynamicviewfti = buildPythonPackage rec {
    name = "products.cmfdynamicviewfti-4.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFDynamicViewFTI/Products.CMFDynamicViewFTI-4.0.3.zip";
      md5 = "7d39d416b41b2d93954bc73d9d0e077f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition extensionclass products_cmfcore products_genericsetup setuptools zope_browsermenu zope_component zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfeditions = buildPythonPackage rec {
    name = "products.cmfeditions-2.2.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFEditions/Products.CMFEditions-2.2.7.zip";
      md5 = "7dc744b3b896c1b212d9ba37b1752b65";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime plone_app_blob products_cmfcore products_cmfdifftool products_cmfuid products_genericsetup products_zopeversioncontrol setuptools transaction zodb3 zope_copy zope_dottedname zope_i18nmessageid zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfformcontroller = buildPythonPackage rec {
    name = "products.cmfformcontroller-3.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFFormController/Products.CMFFormController-3.0.3.zip";
      md5 = "6573df7dcb39e3b63ba22abe2acd639e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_cmfcore products_genericsetup setuptools transaction zope_interface zope_structuredtext zope_tales zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfplacefulworkflow = buildPythonPackage rec {
    name = "products.cmfplacefulworkflow-1.5.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFPlacefulWorkflow/Products.CMFPlacefulWorkflow-1.5.9.zip";
      md5 = "9041e1f52eab5b348c0dfa85be438722";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ products_cmfcore products_cmfplone products_genericsetup products_plonetestcase setuptools zope_component zope_i18nmessageid zope_interface zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfplone = buildPythonPackage rec {
    name = "products.cmfplone-4.2.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFPlone/Products.CMFPlone-4.2.4.zip";
      md5 = "9c9663cb2b68c07e3d9a2fceaa97eaa1";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfquickinstallertool = buildPythonPackage rec {
    name = "products.cmfquickinstallertool-3.0.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFQuickInstallerTool/Products.CMFQuickInstallerTool-3.0.6.tar.gz";
      md5 = "af34adb87ddf2b6da48eff8b70ca2989";
    };

    propagatedBuildInputs = [ acquisition datetime products_cmfcore products_genericsetup setuptools zope_annotation zope_component zope_i18nmessageid zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_cmfuid = buildPythonPackage rec {
    name = "products.cmfuid-2.2.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.CMFUid/Products.CMFUid-2.2.1.tar.gz";
      md5 = "e20727959351dffbf0bac80613eee110";
    };

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_contentmigration = buildPythonPackage rec {
    name = "products.contentmigration-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.contentmigration/Products.contentmigration-2.1.2.zip";
      md5 = "1cef33faec03e655b7c52c317db50ed2";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_dcworkflow = buildPythonPackage rec {
    name = "products.dcworkflow-2.2.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.DCWorkflow/Products.DCWorkflow-2.2.4.tar.gz";
      md5 = "c90a16c4f3611015592ba8173a5f1863";
    };

    propagatedBuildInputs = [ products_cmfcore products_genericsetup setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_extendedpathindex = buildPythonPackage rec {
    name = "products.extendedpathindex-3.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ExtendedPathIndex/Products.ExtendedPathIndex-3.1.zip";
      md5 = "00c048a4b103200bdcbda61fa22c66df";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ accesscontrol setuptools transaction zodb3 zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_externaleditor = buildPythonPackage rec {
    name = "products.externaleditor-1.1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ExternalEditor/Products.ExternalEditor-1.1.0.zip";
      md5 = "475fea6e0b958c0c51cfdbfef2f4e623";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_externalmethod = buildPythonPackage rec {
    name = "products.externalmethod-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ExternalMethod/Products.ExternalMethod-2.13.0.zip";
      md5 = "15ba953ef6cb632eb571977651252ea6";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_genericsetup = buildPythonPackage rec {
    name = "products.genericsetup-1.7.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.GenericSetup/Products.GenericSetup-1.7.3.tar.gz";
      md5 = "c48967c81c880ed33ee16a14caab3b11";
    };

    propagatedBuildInputs = [ five_localsitemanager setuptools zope_formlib zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_kupu = buildPythonPackage rec {
    name = "products.kupu-1.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.kupu/Products.kupu-1.5.1.zip";
      md5 = "b884fcc7f510426974d8d3c4333da4f4";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_outputfilters products_archetypes products_cmfcore products_cmfplone products_genericsetup products_mimetypesregistry products_portaltransforms setuptools zope_app_component zope_i18n zope_i18nmessageid zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_mailhost = buildPythonPackage rec {
    name = "products.mailhost-2.13.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.MailHost/Products.MailHost-2.13.1.zip";
      md5 = "1102e523435d8bf78a15b9ddb57478e1";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_marshall = buildPythonPackage rec {
    name = "products.marshall-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.Marshall/Products.Marshall-2.1.2.zip";
      md5 = "bde4d7f75195c1ded8371554b04d2541";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_mimetools = buildPythonPackage rec {
    name = "products.mimetools-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.MIMETools/Products.MIMETools-2.13.0.zip";
      md5 = "ad5372fc1190599a19493db0864448ec";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ documenttemplate setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_mimetypesregistry = buildPythonPackage rec {
    name = "products.mimetypesregistry-2.0.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.MimetypesRegistry/Products.MimetypesRegistry-2.0.4.zip";
      md5 = "898166bb2aaececc8238ad4ee4826793";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_cmfcore setuptools zodb3 zope_contenttype zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_ofsp = buildPythonPackage rec {
    name = "products.ofsp-2.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.OFSP/Products.OFSP-2.13.2.zip";
      md5 = "c76d40928753c2ee56db873304e65bd5";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_passwordresettool = buildPythonPackage rec {
    name = "products.passwordresettool-2.0.11";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PasswordResetTool/Products.PasswordResetTool-2.0.11.zip";
      md5 = "8dfd65f06c3f4a4b0742d1b44b65f014";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_placelesstranslationservice = buildPythonPackage rec {
    name = "products.placelesstranslationservice-2.0.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PlacelessTranslationService/Products.PlacelessTranslationService-2.0.3.zip";
      md5 = "a94635eb712563c5a002520713f5d6dc";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime extensionclass python_gettext setuptools zodb3 zope_annotation zope_component zope_deferredimport zope_deprecation zope_i18n zope_interface zope_publisher zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_plonelanguagetool = buildPythonPackage rec {
    name = "products.plonelanguagetool-3.2.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PloneLanguageTool/Products.PloneLanguageTool-3.2.7.zip";
      md5 = "bd9eb6278bf76e8cbce99437ca362164";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_plonepas = buildPythonPackage rec {
    name = "products.plonepas-4.0.15";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PlonePAS/Products.PlonePAS-4.0.15.zip";
      md5 = "c19241b558c994ff280a2e1f50aa1f19";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ plone_i18n plone_memoize plone_session products_cmfcore products_genericsetup products_pluggableauthservice setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_plonetestcase = buildPythonPackage rec {
    name = "products.plonetestcase-0.9.15";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PloneTestCase/Products.PloneTestCase-0.9.15.zip";
      md5 = "ddd5810937919ab5233ebd64893c8bae";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition products_atcontenttypes products_cmfcore products_cmfplone products_genericsetup setuptools zodb3 zope_component zope_interface zope_site zope_testing zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_pluggableauthservice = buildPythonPackage rec {
    name = "products.pluggableauthservice-1.9.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PluggableAuthService/Products.PluggableAuthService-1.9.0.tar.gz";
      md5 = "f78f16e46d016c2848bc84254fa66596";
    };

    propagatedBuildInputs = [ products_genericsetup products_pluginregistry setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_pluginregistry = buildPythonPackage rec {
    name = "products.pluginregistry-1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PluginRegistry/Products.PluginRegistry-1.3.tar.gz";
      md5 = "5b166193ca1eb84dfb402051f779ebab";
    };

    propagatedBuildInputs = [ products_genericsetup setuptools zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_portaltransforms = buildPythonPackage rec {
    name = "products.portaltransforms-2.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PortalTransforms/Products.PortalTransforms-2.1.2.zip";
      md5 = "9f429f3c3b9e0019d0f6c9b7a8a9376e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition markdown plone_intelligenttext products_cmfcore products_cmfdefault products_mimetypesregistry setuptools zodb3 zope_interface zope_structuredtext zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_pythonscripts = buildPythonPackage rec {
    name = "products.pythonscripts-2.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.PythonScripts/Products.PythonScripts-2.13.2.zip";
      md5 = "04c86f2c45a29a162297a80dac61d14f";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_resourceregistries = buildPythonPackage rec {
    name = "products.resourceregistries-2.2.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ResourceRegistries/Products.ResourceRegistries-2.2.6.zip";
      md5 = "9cf6efbcf2a6510033c06e1d3af94080";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime plone_app_registry products_cmfcore products_genericsetup setuptools zodb3 zope_component zope_interface zope_viewlet zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_securemailhost = buildPythonPackage rec {
    name = "products.securemailhost-1.1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.SecureMailHost/Products.SecureMailHost-1.1.2.zip";
      md5 = "7db0f1fa867bd0df972082f502a7a707";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_standardcachemanagers = buildPythonPackage rec {
    name = "products.standardcachemanagers-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.StandardCacheManagers/Products.StandardCacheManagers-2.13.0.zip";
      md5 = "c5088b2b62bd26d63d9579a04369cb73";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_statusmessages = buildPythonPackage rec {
    name = "products.statusmessages-4.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.statusmessages/Products.statusmessages-4.0.zip";
      md5 = "265324b0a58a032dd0ed038103ed0473";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_annotation zope_i18n zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_tinymce = buildPythonPackage rec {
    name = "products.tinymce-1.2.15";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.TinyMCE/Products.TinyMCE-1.2.15.zip";
      md5 = "108b919bfcff711d2116e41eccbede58";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ elementtree plone_app_imaging plone_outputfilters setuptools zope_app_component zope_app_content ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_validation = buildPythonPackage rec {
    name = "products.validation-2.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.validation/Products.validation-2.0.zip";
      md5 = "afa217e2306637d1dccbebf337caa8bf";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime setuptools zope_i18n zope_i18nmessageid zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_zcatalog = buildPythonPackage rec {
    name = "products.zcatalog-2.13.23";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ZCatalog/Products.ZCatalog-2.13.23.zip";
      md5 = "d425171516dfc70e543a4e2b852301cb";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_zctextindex = buildPythonPackage rec {
    name = "products.zctextindex-2.13.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ZCTextIndex/Products.ZCTextIndex-2.13.4.zip";
      md5 = "8bbfa5fcd3609246990a9314d6f826b4";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_zopeversioncontrol = buildPythonPackage rec {
    name = "products.zopeversioncontrol-1.1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ZopeVersionControl/Products.ZopeVersionControl-1.1.3.zip";
      md5 = "238239102f3ac798ee4f4c53343a561f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime setuptools transaction zodb3 zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  products_zsqlmethods = buildPythonPackage rec {
    name = "products.zsqlmethods-2.13.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/P/Products.ZSQLMethods/Products.ZSQLMethods-2.13.4.zip";
      md5 = "bd1ad8fd4a9d4f8b4681401dd5b71dc1";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ acquisition datetime extensionclass missing persistence record setuptools transaction zodb3 zope_interface zope2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  python_dateutil = buildPythonPackage rec {
    name = "python-dateutil-1.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/python-dateutil/${name}.tar.gz";
      md5 = "0dcb1de5e5cad69490a3b6ab63f0cfa5";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  python_gettext = buildPythonPackage rec {
    name = "python-gettext-1.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/python-gettext/${name}.zip";
      md5 = "cd4201d440126d1296d1d2bc2b4795f3";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ unittest2 ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  python_openid = buildPythonPackage rec {
    name = "python-openid-2.2.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/python-openid/${name}.zip";
      md5 = "f89d9d4f4dccfd33b5ce34eb4725f751";
    };

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  pytz = buildPythonPackage rec {
    name = "pytz-2012c";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/p/pytz/pytz-2012c.tar.gz";
      md5 = "1aa85f072e3d34ae310665967a0ce053";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  record = buildPythonPackage rec {
    name = "record-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/R/Record/Record-2.13.0.zip";
      md5 = "cfed6a89d4fb2c9cb995e9084c3071b7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ extensionclass ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  repoze_xmliter = buildPythonPackage rec {
    name = "repoze.xmliter-0.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/r/repoze.xmliter/${name}.zip";
      md5 = "99da76bcbad6fbaced4a273bde29b10e";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ lxml setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  restrictedpython = buildPythonPackage rec {
    name = "restrictedpython-3.6.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/R/RestrictedPython/RestrictedPython-3.6.0.zip";
      md5 = "aa75a7dcc7fbc966357837cc66cacec6";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  setuptools = buildPythonPackage rec {
    name = "setuptools-0.6c11";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/s/setuptools/${name}.tar.gz";
      md5 = "7df2a529a074f613b509fb44feefe74e";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  tempstorage = buildPythonPackage rec {
    name = "tempstorage-2.12.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/t/tempstorage/${name}.zip";
      md5 = "7a2b76b39839e229249b1bb175604480";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  transaction = buildPythonPackage rec {
    name = "transaction-1.1.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/t/transaction/${name}.tar.gz";
      md5 = "30b062baa34fe1521ad979fb088c8c55";
    };

    propagatedBuildInputs = [ zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  unidecode = buildPythonPackage rec {
    name = "unidecode-0.04.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/U/Unidecode/Unidecode-0.04.12.tar.gz";
      md5 = "351dc98f4512bdd2e93f7a6c498730eb";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  unittest2 = buildPythonPackage rec {
    name = "unittest2-0.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/u/unittest2/${name}.tar.gz";
      md5 = "a0af5cac92bbbfa0c3b0e99571390e0f";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  wicked = buildPythonPackage rec {
    name = "wicked-1.1.10";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/w/wicked/${name}.zip";
      md5 = "f65611f11d547d7dc8e623bf87d3929d";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_container zope_lifecycleevent zope_schema zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_autoinclude = buildPythonPackage rec {
    name = "z3c.autoinclude-0.3.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.autoinclude/${name}.zip";
      md5 = "6a615ae18c12b459bceb3ae28e8e7709";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zc_buildout zope_configuration zope_dottedname zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_batching = buildPythonPackage rec {
    name = "z3c.batching-1.1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.batching/${name}.tar.gz";
      md5 = "d1dc834781d228127ca6d15301757863";
    };

    propagatedBuildInputs = [ setuptools zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_caching = buildPythonPackage rec {
    name = "z3c.cachingzcml-2.0a1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.caching/z3c.caching-2.0a1.tar.gz";
      md5 = "17f250b5084c2324a7d15c6810ee628e";
    };

    propagatedBuildInputs = [ setuptools zope_browser zope_component zope_event zope_interface zope_lifecycleevent zope_configuration ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_form = buildPythonPackage rec {
    name = "z3c.form-2.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.form/${name}.tar.gz";
      md5 = "f029f83dd226f695f55049ed1ecee95e";
    };

    propagatedBuildInputs = [ setuptools zope_browser zope_component zope_configuration zope_contentprovider zope_event zope_i18n zope_i18nmessageid zope_interface zope_lifecycleevent zope_location zope_pagetemplate zope_publisher zope_schema zope_security zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_formwidget_query = buildPythonPackage rec {
    name = "z3c.formwidget.query-0.9";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.formwidget.query/${name}.zip";
      md5 = "d9f7960b1a5a81d8ba5241530f496522";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools z3c_form zope_component zope_i18nmessageid zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  z3c_zcmlhook = buildPythonPackage rec {
    name = "z3c.zcmlhook-1.0b1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/z3c.zcmlhook/${name}.tar.gz";
      md5 = "7b6c80146f5930409eb0b355ddf3daeb";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_configuration zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zc_buildout = buildPythonPackage rec {
    name = "zc.buildout-1.7.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zc.buildout/${name}.tar.gz";
      md5 = "4e3b521600e475c56a0a66459a5fc7bb";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zc_lockfile = buildPythonPackage rec {
    name = "zc.lockfile-1.0.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zc.lockfile/${name}.tar.gz";
      md5 = "6cf83766ef9935c33e240b0904c7a45e";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zconfig = buildPythonPackage rec {
    name = "zconfig-2.9.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZConfig/ZConfig-2.9.0.zip";
      md5 = "5c932690a70c8907efd240cdd76a7bc4";
    };

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zdaemon = buildPythonPackage rec {
    name = "zdaemon-2.0.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zdaemon/${name}.tar.gz";
      md5 = "291a875f82e812110557eb6704af8afe";
    };

    propagatedBuildInputs = [ zconfig ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zexceptions = buildPythonPackage rec {
    name = "zexceptions-2.13.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zExceptions/zExceptions-2.13.0.zip";
      md5 = "4c679696c959040d8e656ef85ae40136";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_interface zope_publisher zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zlog = buildPythonPackage rec {
    name = "zlog-2.11.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zLOG/zLOG-2.11.1.tar.gz";
      md5 = "68073679aaa79ac5a7b6a5c025467147";
    };

    propagatedBuildInputs = [ zconfig ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zodb3 = buildPythonPackage rec {
    name = "zodb3-3.10.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZODB3/ZODB3-3.10.5.tar.gz";
      md5 = "6f180c6897a1820948fee2a6290503cd";
    };

    propagatedBuildInputs = [ transaction zc_lockfile zconfig zdaemon zope_event zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope2 = buildPythonPackage rec {
    name = "zope2-2.13.19";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/Zope2/Zope2-2.13.19.zip";
      md5 = "26fee311aace7c12e406543ea91eb42a";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_annotation = buildPythonPackage rec {
    name = "zope.annotation-3.5.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.annotation/${name}.tar.gz";
      md5 = "4238153279d3f30ab5613438c8e76380";
    };

    propagatedBuildInputs = [ setuptools zodb3 zope_component zope_interface zope_location zope_proxy ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_cache = buildPythonPackage rec {
    name = "zope.app.cache-3.7.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.cache/${name}.zip";
      md5 = "8dd74574e869ce236ced0de7e349bb5c";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_annotation zope_app_form zope_app_pagetemplate zope_component zope_componentvocabulary zope_interface zope_proxy zope_publisher zope_ramcache zope_schema zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_component = buildPythonPackage rec {
    name = "zope.app.component-3.9.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.component/${name}.tar.gz";
      md5 = "bc2dce245d2afe462529c350956711e0";
    };

    propagatedBuildInputs = [ setuptools zope_app_container zope_app_pagetemplate zope_component zope_componentvocabulary zope_deprecation zope_exceptions zope_formlib zope_i18nmessageid zope_interface zope_publisher zope_schema zope_security zope_site zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_container = buildPythonPackage rec {
    name = "zope.app.container-3.9.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.container/${name}.tar.gz";
      md5 = "1e286c59f0166e517d67ddd723641c84";
    };

    propagatedBuildInputs = [ setuptools zope_browser zope_browsermenu zope_browserpage zope_component zope_container zope_copypastemove zope_dublincore zope_event zope_exceptions zope_i18n zope_i18nmessageid zope_interface zope_lifecycleevent zope_location zope_publisher zope_security zope_size zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_content = buildPythonPackage rec {
    name = "zope.app.content-3.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.content/${name}.tar.gz";
      md5 = "0ac6a6fcb5dd6f845759f998d8e8cbb3";
    };

    propagatedBuildInputs = [ setuptools zope_componentvocabulary zope_interface zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_form = buildPythonPackage rec {
    name = "zope.app.form-4.0.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.form/${name}.tar.gz";
      md5 = "3d2b164d9d37a71490a024aaeb412e91";
    };

    propagatedBuildInputs = [ setuptools transaction zope_browser zope_browsermenu zope_browserpage zope_component zope_configuration zope_datetime zope_exceptions zope_formlib zope_i18n zope_interface zope_proxy zope_publisher zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_locales = buildPythonPackage rec {
    name = "zope.app.locales-3.6.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.locales/${name}.tar.gz";
      md5 = "bd2b4c6040e768f33004b1210d3207fa";
    };

    propagatedBuildInputs = [ setuptools zope_i18nmessageid zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_pagetemplate = buildPythonPackage rec {
    name = "zope.app.pagetemplate-3.11.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.pagetemplate/${name}.tar.gz";
      md5 = "2d304729c0d6a9ab67dd5ea852f19476";
    };

    propagatedBuildInputs = [ setuptools zope_browserpage zope_component zope_configuration zope_dublincore zope_i18nmessageid zope_interface zope_pagetemplate zope_schema zope_security zope_size zope_tales zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_publication = buildPythonPackage rec {
    name = "zope.app.publication-3.12.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.publication/${name}.zip";
      md5 = "d8c521287f52fb9f40fa9b8c2acb4675";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_authentication zope_browser zope_component zope_error zope_interface zope_location zope_publisher zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_app_publisher = buildPythonPackage rec {
    name = "zope.app.publisher-3.10.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.app.publisher/${name}.zip";
      md5 = "66e9110e2967d8d204a65a98e2227404";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_browsermenu zope_browserpage zope_browserresource zope_component zope_componentvocabulary zope_configuration zope_datetime zope_interface zope_location zope_ptresource zope_publisher zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_authentication = buildPythonPackage rec {
    name = "zope.authentication-3.7.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.authentication/${name}.zip";
      md5 = "7d6bb340610518f2fc71213cfeccda68";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_browser zope_component zope_i18nmessageid zope_interface zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_broken = buildPythonPackage rec {
    name = "zope.broken-3.6.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.broken/${name}.zip";
      md5 = "eff24d7918099a3e899ee63a9c31bee6";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_browser = buildPythonPackage rec {
    name = "zope.browser-1.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.browser/${name}.zip";
      md5 = "4ff0ddbf64c45bfcc3189e35f4214ded";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_browsermenu = buildPythonPackage rec {
    name = "zope.browsermenu-3.9.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.browsermenu/${name}.zip";
      md5 = "a47c7b1e786661c912a1150bf8d1f83f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_browser zope_component zope_configuration zope_i18nmessageid zope_interface zope_pagetemplate zope_publisher zope_schema zope_security zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_browserpage = buildPythonPackage rec {
    name = "zope.browserpage-3.12.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.browserpage/${name}.tar.gz";
      md5 = "a543ef3cb1b42f7233b3fca23dc9ea60";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_configuration zope_interface zope_pagetemplate zope_publisher zope_schema zope_security zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_browserresource = buildPythonPackage rec {
    name = "zope.browserresource-3.10.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.browserresource/${name}.zip";
      md5 = "dbfde30e82dbfa1a74c5da0cb5a4772d";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_component zope_configuration zope_contenttype zope_i18n zope_interface zope_location zope_publisher zope_schema zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_cachedescriptors = buildPythonPackage rec {
    name = "zope.cachedescriptors-3.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.cachedescriptors/${name}.zip";
      md5 = "263459a95238fd61d17e815d97ca49ce";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_component = buildPythonPackage rec {
    name = "zope.componenthook-zcml-3.9.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.component/zope.component-3.9.5.tar.gz";
      md5 = "22780b445b1b479701c05978055d1c82";
    };

    propagatedBuildInputs = [ setuptools zope_event zope_interface zope_hookable zope_configuration zope_i18nmessageid ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_componentvocabulary = buildPythonPackage rec {
    name = "zope.componentvocabulary-1.0.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.componentvocabulary/${name}.tar.gz";
      md5 = "1c8fa82ca1ab1f4b0bd2455a31fde22b";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_i18nmessageid zope_interface zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_configuration = buildPythonPackage rec {
    name = "zope.configuration-3.7.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.configuration/${name}.zip";
      md5 = "5b0271908ef26c05059eda76928896ea";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_i18nmessageid zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_container = buildPythonPackage rec {
    name = "zope.container-3.11.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.container/${name}.tar.gz";
      md5 = "fc66d85a17b8ffb701091c9328983dcc";
    };

    propagatedBuildInputs = [ setuptools zodb3 zope_broken zope_component zope_dottedname zope_event zope_filerepresentation zope_i18nmessageid zope_interface zope_lifecycleevent zope_location zope_publisher zope_schema zope_security zope_size zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_contentprovider = buildPythonPackage rec {
    name = "zope.contentprovider-3.7.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.contentprovider/${name}.tar.gz";
      md5 = "1bb2132551175c0123f17939a793f812";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_event zope_interface zope_location zope_publisher zope_schema zope_tales ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_contenttype = buildPythonPackage rec {
    name = "zope.contenttype-3.5.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.contenttype/${name}.zip";
      md5 = "c6ac80e6887de4108a383f349fbdf332";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_copy = buildPythonPackage rec {
    name = "zope.copy-3.5.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.copy/${name}.tar.gz";
      md5 = "a9836a5d36cd548be45210eb00407337";
    };

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_copypastemove = buildPythonPackage rec {
    name = "zope.copypastemove-3.7.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.copypastemove/${name}.tar.gz";
      md5 = "f335940686d15cfc5520c42f2494a924";
    };

    propagatedBuildInputs = [ setuptools zope_annotation zope_component zope_container zope_copy zope_event zope_exceptions zope_interface zope_lifecycleevent zope_location ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_datetime = buildPythonPackage rec {
    name = "zope.datetime-3.4.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.datetime/${name}.tar.gz";
      md5 = "4dde22d34f41a0a4f0c5a345e6d11ee9";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_deferredimport = buildPythonPackage rec {
    name = "zope.deferredimport-3.5.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.deferredimport/${name}.tar.gz";
      md5 = "68fce3bf4f011d4a840902fd763884ee";
    };

    propagatedBuildInputs = [ setuptools zope_proxy ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_deprecation = buildPythonPackage rec {
    name = "zope.deprecation-3.4.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.deprecation/${name}.tar.gz";
      md5 = "8a47b0f8e1fa4e833007e5b8351bb1d4";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_dottedname = buildPythonPackage rec {
    name = "zope.dottedname-3.4.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.dottedname/${name}.tar.gz";
      md5 = "62d639f75b31d2d864fe5982cb23959c";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_dublincore = buildPythonPackage rec {
    name = "zope.dublincore-3.7.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.dublincore/${name}.tar.gz";
      md5 = "2e34e42e454d896feb101ac74af62ded";
    };

    propagatedBuildInputs = [ pytz setuptools zope_component zope_datetime zope_interface zope_lifecycleevent zope_location zope_schema zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_error = buildPythonPackage rec {
    name = "zope.error-3.7.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.error/${name}.tar.gz";
      md5 = "281445a906458ff5f18f56923699a127";
    };

    propagatedBuildInputs = [ setuptools zodb3 zope_exceptions zope_interface zope_location ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_event = buildPythonPackage rec {
    name = "zope.event-3.5.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.event/${name}.tar.gz";
      md5 = "6e8af2a16157a74885d4f0d88137cefb";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_exceptions = buildPythonPackage rec {
    name = "zope.exceptions-3.6.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.exceptions/${name}.tar.gz";
      md5 = "d7234d99d728abe3d9275346e8d24fd9";
    };

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_filerepresentation = buildPythonPackage rec {
    name = "zope.filerepresentation-3.6.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.filerepresentation/${name}.tar.gz";
      md5 = "4a7a434094f4bfa99a7f22e75966c359";
    };

    propagatedBuildInputs = [ setuptools zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_formlib = buildPythonPackage rec {
    name = "zope.formlib-4.0.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.formlib/${name}.zip";
      md5 = "eed9c94382d11a4dececd0a48ac1d3f2";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ pytz setuptools zope_browser zope_browserpage zope_component zope_datetime zope_event zope_i18n zope_i18nmessageid zope_interface zope_lifecycleevent zope_publisher zope_schema zope_security zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_globalrequest = buildPythonPackage rec {
    name = "zope.globalrequest-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.globalrequest/${name}.zip";
      md5 = "ae6ff02db5ba89c1fb96ed7a73ca1cfa";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_hookable = buildPythonPackage rec {
    name = "zope.hookable-3.4.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.hookable/${name}.tar.gz";
      md5 = "fe6713aef5b6c0f4963fb984bf326da0";
    };

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_i18n = buildPythonPackage rec {
    name = "zope.i18nzcml-3.7.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.i18n/zope.i18n-3.7.4.tar.gz";
      md5 = "a6fe9d9ad53dd7e94e87cd58fb67d3b7";
    };

    # circular dependencies
    installCommand = 'easy_install --always-unzip --no-deps --prefix="$out" .'

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_i18nmessageid = buildPythonPackage rec {
    name = "zope.i18nmessageid-3.5.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.i18nmessageid/${name}.tar.gz";
      md5 = "cb84bf61c2b7353e3b7578057fbaa264";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_interface = buildPythonPackage rec {
    name = "zope.interface-3.6.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.interface/${name}.zip";
      md5 = "9df962180fbbb54eb1875cff9fe436e5";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_lifecycleevent = buildPythonPackage rec {
    name = "zope.lifecycleevent-3.6.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.lifecycleevent/${name}.tar.gz";
      md5 = "3ba978f3ba7c0805c81c2c79ea3edb33";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_event zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_location = buildPythonPackage rec {
    name = "zope.location-3.9.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.location/${name}.tar.gz";
      md5 = "1684a8f986099d15296f670c58e713d8";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_interface zope_proxy zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_pagetemplate = buildPythonPackage rec {
    name = "zope.pagetemplate-3.6.3";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.pagetemplate/${name}.zip";
      md5 = "834a4bf702c05fba1e669677b4dc871f";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_component zope_i18n zope_i18nmessageid zope_interface zope_security zope_tal zope_tales zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_processlifetime = buildPythonPackage rec {
    name = "zope.processlifetime-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.processlifetime/${name}.tar.gz";
      md5 = "69604bfd668a01ebebdd616a8f26ccfe";
    };

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_proxy = buildPythonPackage rec {
    name = "zope.proxy-3.6.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.proxy/${name}.zip";
      md5 = "a400b0a26624b17fa889dbcaa989d440";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_ptresource = buildPythonPackage rec {
    name = "zope.ptresource-3.9.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.ptresource/${name}.tar.gz";
      md5 = "f4645e51c15289d3fdfb4139039e18e9";
    };

    propagatedBuildInputs = [ setuptools zope_browserresource zope_interface zope_pagetemplate zope_publisher zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_publisher = buildPythonPackage rec {
    name = "zope.publisher-3.12.6";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.publisher/${name}.tar.gz";
      md5 = "495131970cc7cb14de8e517fb3857ade";
    };

    propagatedBuildInputs = [ setuptools zope_browser zope_component zope_configuration zope_contenttype zope_event zope_exceptions zope_i18n zope_interface zope_location zope_proxy zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_ramcache = buildPythonPackage rec {
    name = "zope.ramcache-1.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.ramcache/${name}.zip";
      md5 = "87289e15f0e51f50704adda1557c02a7";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zodb3 zope_interface zope_location zope_testing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_schema = buildPythonPackage rec {
    name = "zope.schema-4.2.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.schema/${name}.zip";
      md5 = "bfa0460b68df0dbbf7a5dc793b0eecc6";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_event zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_security = buildPythonPackage rec {
    name = "zope.securityuntrustedpython-3.7.4";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.security/zope.security-3.7.4.tar.gz";
      md5 = "072ab8d11adc083eace11262da08630c";
    };

    propagatedBuildInputs = [ setuptools zope_component zope_configuration zope_i18nmessageid zope_interface zope_location zope_proxy zope_schema restrictedpython ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_sendmail = buildPythonPackage rec {
    name = "zope.sendmail-3.7.5";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.sendmail/${name}.tar.gz";
      md5 = "8a513ecf2b41cad849f6607bf16d6818";
    };

    propagatedBuildInputs = [ setuptools transaction zope_component zope_configuration zope_i18nmessageid zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_sequencesort = buildPythonPackage rec {
    name = "zope.sequencesort-3.4.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.sequencesort/${name}.tar.gz";
      md5 = "cfc35fc426a47f5c0ee43c416224b864";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_site = buildPythonPackage rec {
    name = "zope.site-3.9.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.site/${name}.tar.gz";
      md5 = "36a0b8dfbd713ed452ce6973ab0a3ddb";
    };

    propagatedBuildInputs = [ setuptools zope_annotation zope_component zope_container zope_event zope_interface zope_lifecycleevent zope_location zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_size = buildPythonPackage rec {
    name = "zope.size-3.4.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.size/${name}.tar.gz";
      md5 = "55d9084dfd9dcbdb5ad2191ceb5ed03d";
    };

    propagatedBuildInputs = [ setuptools zope_i18nmessageid zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_structuredtext = buildPythonPackage rec {
    name = "zope.structuredtext-3.5.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.structuredtext/${name}.tar.gz";
      md5 = "eabbfb983485d0879322bc878d2478a0";
    };

    propagatedBuildInputs = [ setuptools ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_tal = buildPythonPackage rec {
    name = "zope.tal-3.5.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.tal/${name}.zip";
      md5 = "13869f292ba36b294736b7330b1396fd";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_i18nmessageid zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_tales = buildPythonPackage rec {
    name = "zope.tales-3.5.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.tales/${name}.tar.gz";
      md5 = "1c5060bd766a0a18632b7879fc9e4e1e";
    };

    propagatedBuildInputs = [ setuptools zope_interface zope_tal ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_testbrowser = buildPythonPackage rec {
    name = "zope.testbrowser-3.11.1";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.testbrowser/${name}.tar.gz";
      md5 = "64abbee892121e7f1a91aed12cfc155a";
    };

    propagatedBuildInputs = [ mechanize pytz setuptools zope_interface zope_schema ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_testing = buildPythonPackage rec {
    name = "zope.testing-3.9.7";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.testing/${name}.tar.gz";
      md5 = "8999f3d143d416dc3c8b2a5bd6f33e28";
    };

    propagatedBuildInputs = [ setuptools zope_exceptions zope_interface ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_traversing = buildPythonPackage rec {
    name = "zope.traversing-3.13.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.traversing/${name}.zip";
      md5 = "eaad8fc7bbef126f9f8616b074ec00aa";
    };

    buildInputs = [ pkgs.unzip ];

    propagatedBuildInputs = [ setuptools zope_component zope_i18n zope_i18nmessageid zope_interface zope_location zope_proxy zope_publisher zope_security ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zope_viewlet = buildPythonPackage rec {
    name = "zope.viewlet-3.7.2";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/z/zope.viewlet/${name}.tar.gz";
      md5 = "367e03096df57e2f9b74fff43f7901f9";
    };

    propagatedBuildInputs = [ setuptools zope_browserpage zope_component zope_configuration zope_contentprovider zope_event zope_i18nmessageid zope_interface zope_location zope_publisher zope_schema zope_security zope_traversing ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


  zopeundo = buildPythonPackage rec {
    name = "zopeundo-2.12.0";

    src = fetchurl {
      url = "http://pypi.python.org/packages/source/Z/ZopeUndo/ZopeUndo-2.12.0.zip";
      md5 = "2b8da09d1b98d5558f62e12f6e52c401";
    };

    buildInputs = [ pkgs.unzip ];

    meta = {
      maintainers = [
        stdenv.lib.maintainers.chaoflow
        stdenv.lib.maintainers.garbas
        stdenv.lib.maintainers.goibhniu
     ];
    };
  };


}; in plone42Packages

