{ pkgs, self, pythonPackages}:
let
  inherit (pythonPackages) buildPythonPackage;
  inherit (pkgs) fetchurl lib;
in {
   "logan" = buildPythonPackage {
     name = "logan-0.7.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/l/logan/logan-0.7.1.tar.gz";
       md5 = "513673ebd46986d8fb5a0e280c361291";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "nydus" = buildPythonPackage {
     name = "nydus-0.11.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/n/nydus/nydus-0.11.0.tar.gz";
       md5 = "d7a69e5afd9f7606a61168791484d4c3";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."redis" self."mock" ];
     meta = {
     };
   };
   "setuptools" = buildPythonPackage {
     name = "setuptools-18.5";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/setuptools/setuptools-18.5.tar.gz";
       md5 = "533c868f01169a3085177dffe5e768bb";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "redis" = buildPythonPackage {
     name = "redis-2.10.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/r/redis/redis-2.10.3.tar.gz";
       md5 = "7619221ad0cbd124a5687458ea3f5289";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "cryptography" = buildPythonPackage {
     name = "cryptography-1.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/c/cryptography/cryptography-1.1.tar.gz";
       md5 = "dd06da41535184f48f2c8e8b74dd570f";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."ipaddress" self."enum34" self."pyasn1" self."six" self."cffi" self."idna" ];
     meta = {
     };
   };
   "BeautifulSoup" = buildPythonPackage {
     name = "BeautifulSoup-3.2.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/B/BeautifulSoup/BeautifulSoup-3.2.1.tar.gz";
       md5 = "44656527ef3ac9874ac4d1c9f35f70ee";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-crispy-forms" = buildPythonPackage {
     name = "django-crispy-forms-1.4.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-crispy-forms/django-crispy-forms-1.4.0.tar.gz";
       md5 = "b4bc5932405039839e6a99ecf95d30d7";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."Django" ];
     meta = {
     };
   };
   "exam" = buildPythonPackage {
     name = "exam-0.10.5";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/e/exam/exam-0.10.5.tar.gz";
       md5 = "cb5a5848f3779283054d5556a6c16f55";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."mock" ];
     meta = {
     };
   };
   "mock" = buildPythonPackage {
     name = "mock-1.3.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/m/mock/mock-1.3.0.tar.gz";
       md5 = "73ee8a4afb3ff4da1b4afa287f39fdeb";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pbr" self."six" self."funcsigs" ];
     meta = {
     };
   };
   "django-templatetag-sugar" = buildPythonPackage {
     name = "django-templatetag-sugar-1.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-templatetag-sugar/django-templatetag-sugar-1.0.tar.gz";
       md5 = "40da36b5a4bf98fdff867f2ccd5bb34e";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "oauth2" = buildPythonPackage {
     name = "oauth2-1.9.0.post1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/o/oauth2/oauth2-1.9.0.post1.tar.gz";
       md5 = "22d49051d1d19d9ec17df480a463d0bb";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."httplib2" ];
     meta = {
     };
   };
   "django-sudo" = buildPythonPackage {
     name = "django-sudo-1.1.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-sudo/django-sudo-1.1.3.tar.gz";
       md5 = "90e2b75f51d1a9e5fdbdd4873207e11b";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pytest" self."Django" ];
     meta = {
     };
   };
   "raven" = buildPythonPackage {
     name = "raven-5.8.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/r/raven/raven-5.8.1.tar.gz";
       md5 = "455eff0aa70ad1b2d77d20ee7deafb10";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."celery" self."pytest" self."mock" self."exam" self."Django" self."pytz" self."requests" self."pytest-django" self."anyjson" ];
     meta = {
     };
   };
   "amqp" = buildPythonPackage {
     name = "amqp-1.4.7";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/a/amqp/amqp-1.4.7.tar.gz";
       md5 = "5aa44107d142f56385d2375f302cf7b0";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "lxml" = buildPythonPackage {
     name = "lxml-3.4.4";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/l/lxml/lxml-3.4.4.tar.gz";
       md5 = "a9a65972afc173ec7a39c585f4eea69c";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."cssselect" ];
     meta = {
     };
   };
   "wsgiref" = buildPythonPackage {
     name = "wsgiref-0.1.2";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/w/wsgiref/wsgiref-0.1.2.zip";
       md5 = "29b146e6ebd0f9fb119fe321f7bcf6cb";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "simplejson" = buildPythonPackage {
     name = "simplejson-3.3.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/simplejson/simplejson-3.3.3.tar.gz";
       md5 = "38ff12d163e5cc8c592d609820869817";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "ipaddress" = buildPythonPackage {
     name = "ipaddress-1.0.14";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/i/ipaddress/ipaddress-1.0.14.tar.gz";
       md5 = "e2f2f6593b2b8a7e8abba0fbdf33f046";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "email-reply-parser" = buildPythonPackage {
     name = "email-reply-parser-0.2.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/e/email_reply_parser/email_reply_parser-0.2.0.tar.gz";
       md5 = "6fb93cf85eca7916b6e8db6cb67a8f53";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "toronado" = buildPythonPackage {
     name = "toronado-0.0.7";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/t/toronado/toronado-0.0.7.tar.gz";
       md5 = "d96c86ed9f0149382cddf9d5bc18ab75";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."cssutils" self."lxml" self."cssselect" self."exam" self."pytest" ];
     meta = {
     };
   };
   "cssselect" = buildPythonPackage {
     name = "cssselect-0.9.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/c/cssselect/cssselect-0.9.1.tar.gz";
       md5 = "c74f45966277dc7a0f768b9b0f3522ac";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pytest" = buildPythonPackage {
     name = "pytest-2.8.2";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pytest/pytest-2.8.2.tar.gz";
       md5 = "96e77b3a2fb40e5d99a1cfba38ac7c6d";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."py" ];
     meta = {
     };
   };
   "gunicorn" = buildPythonPackage {
     name = "gunicorn-19.3.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/g/gunicorn/gunicorn-19.3.0.tar.gz";
       md5 = "faa3e80661efd67e5e06bba32699af20";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "ipaddr" = buildPythonPackage {
     name = "ipaddr-2.1.11";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/i/ipaddr/ipaddr-2.1.11.tar.gz";
       md5 = "f2c7852f95862715f92e7d089dc3f2cf";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pbr" = buildPythonPackage {
     name = "pbr-1.8.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pbr/pbr-1.8.1.tar.gz";
       md5 = "c8f9285e1a4ca6f9654c529b158baa3a";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-paging" = buildPythonPackage {
     name = "django-paging-0.2.5";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-paging/django-paging-0.2.5.tar.gz";
       md5 = "282ef984815f73ce43189d288b2bae2a";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."django-templatetag-sugar" ];
     meta = {
     };
   };
   "ua-parser" = buildPythonPackage {
     name = "ua-parser-0.5.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/u/ua-parser/ua-parser-0.5.0.tar.gz";
       md5 = "860232934e42c0674ff523921d301e91";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pyasn1" = buildPythonPackage {
     name = "pyasn1-0.1.9";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pyasn1/pyasn1-0.1.9.tar.gz";
       md5 = "f00a02a631d4016818659d1cc38d229a";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-jsonfield" = buildPythonPackage {
     name = "django-jsonfield-0.9.13";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-jsonfield/django-jsonfield-0.9.13.tar.gz";
       md5 = "59711741a3ce1798fd90e841e0b5206e";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pyOpenSSL" = buildPythonPackage {
     name = "pyOpenSSL-0.15.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pyOpenSSL/pyOpenSSL-0.15.1.tar.gz";
       md5 = "f447644afcbd5f0a1f47350fec63a4c6";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."six" self."cryptography" ];
     meta = {
     };
   };
   "enum34" = buildPythonPackage {
     name = "enum34-0.9.23";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/e/enum34/enum34-0.9.23.tar.gz";
       md5 = "cac9d9f00440d03df1d3bf6516d6e878";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "sentry" = buildPythonPackage {
     name = "sentry-7.7.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/sentry/sentry-7.7.1.tar.gz";
       md5 = "402fcd142758a0cf9152fe2ed8c0449b";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."django-paging" self."setproctitle" self."django-templatetag-sugar" self."cssutils" self."django-crispy-forms" self."South" self."logan" self."ua-parser" self."petname" self."django-bitfield" self."gunicorn" self."lxml" self."statsd" self."six" self."ipaddr" self."BeautifulSoup" self."django-picklefield" self."celery" self."djangorestframework" self."pytest" self."kombu" self."django-social-auth" self."mock" self."raven" self."django-recaptcha" self."exam" self."simplejson" self."email-reply-parser" self."urllib3" self."Django" self."django-jsonfield" self."python-dateutil" self."pytest-django" self."django-statsd-mozilla" self."django-sudo" self."enum34" self."redis" self."toronado" self."progressbar" self."nydus" self."python-memcached" ];
     meta = {
     };
   };
   "pytz" = buildPythonPackage {
     name = "pytz-2015.7";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pytz/pytz-2015.7.tar.bz2";
       md5 = "ad650c0ce9150d3b53d29d686c09fdda";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "Markdown" = buildPythonPackage {
     name = "Markdown-2.4.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/M/Markdown/Markdown-2.4.1.tar.gz";
       md5 = "5e13d1b1f1da4838b7a5db157143e334";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "South" = buildPythonPackage {
     name = "South-1.0.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/S/South/South-1.0.1.tar.gz";
       md5 = "9977423e4c4f7ca9345f1428a0a57505";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "python-memcached" = buildPythonPackage {
     name = "python-memcached-1.57";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/python-memcached/python-memcached-1.57.tar.gz";
       md5 = "de21f64b42b2d961f3d4ad7beb5468a1";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."six" ];
     meta = {
     };
   };
   "urllib3" = buildPythonPackage {
     name = "urllib3-1.7.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/u/urllib3/urllib3-1.7.1.tar.gz";
       md5 = "8b05bb2081379fe3c332542aa7c172f3";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pytest-django" = buildPythonPackage {
     name = "pytest-django-2.9.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pytest-django/pytest-django-2.9.1.tar.gz";
       md5 = "3c9dde85e99ec409df209a62b4715e1a";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pytest" ];
     meta = {
     };
   };
   "django-statsd-mozilla" = buildPythonPackage {
     name = "django-statsd-mozilla-0.3.14";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-statsd-mozilla/django-statsd-mozilla-0.3.14.tar.gz";
       md5 = "2e72b3faafe36388677b78b9bbf58429";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."statsd" ];
     meta = {
     };
   };
   "virtualenv" = buildPythonPackage {
     name = "virtualenv-1.11.6";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.11.6.tar.gz";
       md5 = "f61cdd983d2c4e6aeabb70b1060d6f49";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "python-openid" = buildPythonPackage {
     name = "python-openid-2.2.5";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/python-openid/python-openid-2.2.5.tar.gz";
       md5 = "393f48b162ec29c3de9e2973548ea50d";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "billiard" = buildPythonPackage {
     name = "billiard-3.3.0.21";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/b/billiard/billiard-3.3.0.21.tar.gz";
       md5 = "5304a48344d8f7e821d06f57da8af1f4";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "pycparser" = buildPythonPackage {
     name = "pycparser-2.14";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/pycparser/pycparser-2.14.tar.gz";
       md5 = "a2bc8d28c923b4fe2b2c3b4b51a4f935";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-bitfield" = buildPythonPackage {
     name = "django-bitfield-1.7.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-bitfield/django-bitfield-1.7.1.tar.gz";
       md5 = "966fb9d796db0189b6fac7407dc8444c";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."six" self."Django" ];
     meta = {
     };
   };
   "httplib2" = buildPythonPackage {
     name = "httplib2-0.9.2";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/h/httplib2/httplib2-0.9.2.tar.gz";
       md5 = "bd1b1445b3b2dfa7276b09b1a07b7f0e";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "six" = buildPythonPackage {
     name = "six-1.10.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz";
       md5 = "34eed507548117b2ab523ab14b2f8b55";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "djangorestframework" = buildPythonPackage {
     name = "djangorestframework-2.3.14";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/djangorestframework/djangorestframework-2.3.14.tar.gz";
       md5 = "5515567dc032685a6d8b5239bd8fcf8b";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "py" = buildPythonPackage {
     name = "py-1.4.30";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/py/py-1.4.30.tar.gz";
       md5 = "a904aabfe4765cb754f2db84ec7bb03a";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "celery" = buildPythonPackage {
     name = "celery-3.1.19";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/c/celery/celery-3.1.19.tar.gz";
       md5 = "fba8c4b269814dc6dbc36abb0e66c384";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."redis" self."kombu" self."PyYAML" self."pytz" self."pyOpenSSL" self."billiard" ];
     meta = {
     };
   };
   "idna" = buildPythonPackage {
     name = "idna-2.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/i/idna/idna-2.0.tar.gz";
       md5 = "bd17a9d15e755375f48a62c13b25b801";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "kombu" = buildPythonPackage {
     name = "kombu-3.0.26";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/k/kombu/kombu-3.0.26.tar.gz";
       md5 = "dda05763cd4b72a131fe1ef9ba93d542";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."anyjson" self."amqp" ];
     meta = {
     };
   };
   "PyYAML" = buildPythonPackage {
     name = "PyYAML-3.11";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz";
       md5 = "f50e08ef0fe55178479d3a618efe21db";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "requests" = buildPythonPackage {
     name = "requests-2.5.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/r/requests/requests-2.5.3.tar.gz";
       md5 = "23bf4fcc89ea8d353eb5353bb4a475b1";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pyOpenSSL" self."pyasn1" self."ndg-httpsclient" ];
     meta = {
     };
   };
   "Django" = buildPythonPackage {
     name = "Django-1.6.11";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/D/Django/Django-1.6.11.tar.gz";
       md5 = "3bf6086c3b923876d283dc3404e32fdd";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-picklefield" = buildPythonPackage {
     name = "django-picklefield-0.3.2";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-picklefield/django-picklefield-0.3.2.tar.gz";
       md5 = "b2c17ca9e03704ce33890e6aefc7b2e5";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "anyjson" = buildPythonPackage {
     name = "anyjson-0.3.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/a/anyjson/anyjson-0.3.3.tar.gz";
       md5 = "2ea28d6ec311aeeebaf993cb3008b27c";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "setproctitle" = buildPythonPackage {
     name = "setproctitle-1.1.9";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/setproctitle/setproctitle-1.1.9.tar.gz";
       md5 = "95d9e56c69437246460a20804961d70d";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "statsd" = buildPythonPackage {
     name = "statsd-3.1";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/s/statsd/statsd-3.1.tar.gz";
       md5 = "8f7b49412b09b2fedb2c8c70f0f10192";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "cssutils" = buildPythonPackage {
     name = "cssutils-0.9.10";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/c/cssutils/cssutils-0.9.10.zip";
       md5 = "81b5c0294c54479a54548769eaa236f8";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "ndg-httpsclient" = buildPythonPackage {
     name = "ndg-httpsclient-0.4.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/n/ndg-httpsclient/ndg_httpsclient-0.4.0.tar.gz";
       md5 = "81972c0267d5a47d678211ac854838f5";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pyasn1" ];
     meta = {
     };
   };
   "python-dateutil" = buildPythonPackage {
     name = "python-dateutil-2.4.2";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.4.2.tar.gz";
       md5 = "4ef68e1c485b09e9f034e10473e5add2";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."six" ];
     meta = {
     };
   };
   "cffi" = buildPythonPackage {
     name = "cffi-1.3.0";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/c/cffi/cffi-1.3.0.tar.gz";
       md5 = "a40ed8c8ac653c8fc7d5603711b06eaf";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."pycparser" ];
     meta = {
     };
   };
   "progressbar" = buildPythonPackage {
     name = "progressbar-2.3";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/progressbar/progressbar-2.3.tar.gz";
       md5 = "cb6359e54edbb5a1ede42f2b3da5fd75";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-social-auth" = buildPythonPackage {
     name = "django-social-auth-0.7.28";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-social-auth/django-social-auth-0.7.28.tar.gz";
       md5 = "50fb14cc829fc28d6021e711e206f228";
     };
     doCheck = false;
     propagatedBuildInputs = [ self."python-openid" self."oauth2" self."Django" ];
     meta = {
     };
   };
   "petname" = buildPythonPackage {
     name = "petname-1.7";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/p/petname/petname-1.7.tar.gz";
       md5 = "13ee130d1e5508b1442d913ed8b6466f";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "funcsigs" = buildPythonPackage {
     name = "funcsigs-0.4";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/f/funcsigs/funcsigs-0.4.tar.gz";
       md5 = "fb1d031f284233e09701f6db1281c2a5";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
   "django-recaptcha" = buildPythonPackage {
     name = "django-recaptcha-1.0.4";
     src = fetchurl {
       url = "https://pypi.python.org/packages/source/d/django-recaptcha/django-recaptcha-1.0.4.tar.gz";
       md5 = "65c7c8d62688fb569525ef380f0008c8";
     };
     doCheck = false;
     propagatedBuildInputs = [  ];
     meta = {
     };
   };
}
