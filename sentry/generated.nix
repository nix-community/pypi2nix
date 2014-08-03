python: self:
{

  "BeautifulSoup".meta.description = "HTML/XML parser for quick-turnaround applications like screen-scraping.";
  "BeautifulSoup".meta.homepage = "http://www.crummy.com/software/BeautifulSoup/";
  "BeautifulSoup".meta.license = "BSD";
  "BeautifulSoup".requires = [];

  "Django".meta.description = "A high-level Python Web framework that encourages rapid development and clean, pragmatic design.";
  "Django".meta.homepage = "http://www.djangoproject.com/";
  "Django".meta.license = "BSD";
  "Django".requires = [];

  "Pygments".meta.description = "Pygments is a syntax highlighting package written in Python.";
  "Pygments".meta.homepage = "http://pygments.org/";
  "Pygments".meta.license = "BSD License";
  "Pygments".requires = [];

  "South".meta.description = "South: Migrations for Django";
  "South".meta.homepage = "http://south.aeracode.org/";
  "South".requires = [];

  "amqp".meta.description = "Low-level AMQP client for Python (fork of amqplib)";
  "amqp".meta.homepage = "http://github.com/celery/py-amqp";
  "amqp".meta.license = "LGPL";
  "amqp".requires = [];

  "anyjson".meta.description = "Wraps the best available JSON implementation available in a common interface";
  "anyjson".meta.homepage = "http://bitbucket.org/runeh/anyjson/";
  "anyjson".meta.license = "BSD";
  "anyjson".requires = [];

  "billiard".meta.description = "Python multiprocessing fork with improvements and bugfixes";
  "billiard".meta.homepage = "http://github.com/celery/billiard";
  "billiard".meta.license = "BSD";
  "billiard".requires = [];

  "celery".meta.description = "Distributed Task Queue";
  "celery".meta.homepage = "http://celeryproject.org";
  "celery".meta.license = "BSD";
  "celery".requires = [self.billiard self.python-dateutil self.kombu];

  "cssutils".meta.description = "A CSS Cascading Style Sheets library for Python";
  "cssutils".meta.homepage = "http://cthedot.de/cssutils/";
  "cssutils".meta.license = "LGPL 2.1 or later, see also http://cthedot.de/cssutils/";
  "cssutils".requires = [];

  "django-celery".meta.description = "Django Celery Integration.";
  "django-celery".meta.homepage = "http://celeryproject.org";
  "django-celery".meta.license = "BSD";
  "django-celery".requires = [self.pytz self.celery];

  "django-crispy-forms".meta.description = "Best way to have Django DRY forms";
  "django-crispy-forms".meta.homepage = "http://github.com/maraujop/django-crispy-forms";
  "django-crispy-forms".meta.license = "MIT";
  "django-crispy-forms".requires = [self.Django];

  "django-paging".meta.description = "An efficient paginator that works.";
  "django-paging".meta.homepage = "http://github.com/dcramer/django-paging";
  "django-paging".requires = [self.django-templatetag-sugar];

  "django-picklefield".meta.description = "Pickled object field for Django";
  "django-picklefield".meta.homepage = "http://github.com/gintas/django-picklefield";
  "django-picklefield".requires = [self.six];

  "django-social-auth".meta.description = "Django social authentication made simple.";
  "django-social-auth".meta.homepage = "https://github.com/omab/django-social-auth";
  "django-social-auth".meta.license = "BSD";
  "django-social-auth".requires = [self.Django self.oauth2 self.python-openid];

  "django-static-compiler".meta.description = "A static file compiler for Django";
  "django-static-compiler".meta.homepage = "http://github.com/dcramer/django-static-compiler";
  "django-static-compiler".meta.license = "Apache License 2.0";
  "django-static-compiler".requires = [];

  "django-templatetag-sugar".meta.description = "A library to make Django's template tags sweet.";
  "django-templatetag-sugar".meta.homepage = "http://github.com/alex/django-templatetag-sugar/";
  "django-templatetag-sugar".meta.license = "BSD";
  "django-templatetag-sugar".requires = [];

  "email-reply-parser".meta.description = "Email reply parser";
  "email-reply-parser".meta.homepage = "https://github.com/zapier/email-reply-parser";
  "email-reply-parser".meta.license = "MIT";
  "email-reply-parser".requires = [];

  "gunicorn".meta.description = "WSGI HTTP Server for UNIX";
  "gunicorn".meta.homepage = "http://gunicorn.org";
  "gunicorn".meta.license = "MIT";
  "gunicorn".requires = [];

  "httpagentparser".meta.description = "Extracts OS Browser etc information from http user agent string";
  "httpagentparser".meta.homepage = "https://github.com/shon/httpagentparser";
  "httpagentparser".meta.license = "http://www.opensource.org/licenses/mit-license.php";
  "httpagentparser".requires = [];

  "httplib2".meta.description = "A comprehensive HTTP client library.";
  "httplib2".meta.homepage = "http://code.google.com/p/httplib2/";
  "httplib2".meta.license = "MIT";
  "httplib2".requires = [];

  "kombu".meta.description = "Messaging Framework for Python";
  "kombu".meta.homepage = "http://kombu.readthedocs.org";
  "kombu".requires = [self.anyjson self.amqp];

  "logan".meta.description = "Logan is a toolkit for building standalone Django applications.";
  "logan".meta.homepage = "http://github.com/dcramer/logan";
  "logan".meta.license = "Apache License 2.0";
  "logan".requires = [];

  "nydus".meta.description = "Connection utilities";
  "nydus".meta.homepage = "http://github.com/disqus/nydus";
  "nydus".meta.license = "Apache License 2.0";
  "nydus".requires = [self.redis];

  "oauth2".meta.description = "library for OAuth version 1.0";
  "oauth2".meta.homepage = "http://github.com/simplegeo/python-oauth2";
  "oauth2".meta.license = "MIT License";
  "oauth2".requires = [self.httplib2];

  "pynliner".meta.description = "Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils";
  "pynliner".requires = [self.BeautifulSoup self.cssutils];

  "python-dateutil".meta.description = "Extensions to the standard python 2.3+ datetime module";
  "python-dateutil".meta.homepage = "http://labix.org/python-dateutil";
  "python-dateutil".meta.license = "PSF License";
  "python-dateutil".requires = [];

  "python-memcached".meta.description = "Pure python memcached client";
  "python-memcached".meta.homepage = "http://www.tummy.com/Community/software/python-memcached/";
  "python-memcached".requires = [];

  "python-openid".meta.description = "OpenID support for servers and consumers.";
  "python-openid".meta.homepage = "http://github.com/openid/python-openid";
  "python-openid".requires = [];

  "pytz".meta.description = "World timezone definitions, modern and historical";
  "pytz".meta.homepage = "http://pythonhosted.org/pytz";
  "pytz".meta.license = "MIT";
  "pytz".requires = [];

  "raven".meta.description = "Raven is a client for Sentry (https://www.getsentry.com)";
  "raven".meta.homepage = "http://github.com/getsentry/raven-python";
  "raven".meta.license = "BSD";
  "raven".requires = [self.celery self.Django self.django-celery self.pytz self.anyjson];

  "redis".meta.description = "Python client for Redis key-value store";
  "redis".meta.homepage = "http://github.com/andymccurdy/redis-py";
  "redis".meta.license = "MIT";
  "redis".requires = [];

  "sentry".meta.description = "A realtime logging and aggregation server.";
  "sentry".meta.homepage = "https://www.getsentry.com";
  "sentry".meta.license = "BSD";
  "sentry".requires = [self.BeautifulSoup self.celery self.cssutils self.Django self.django-celery self.django-crispy-forms self.django-paging self.django-picklefield self.django-social-auth self.django-static-compiler self.django-templatetag-sugar self.email-reply-parser self.gunicorn self.httpagentparser self.logan self.nydus self.Pygments self.pynliner self.python-dateutil self.python-memcached self.raven self.redis self.simplejson self.setproctitle self.South self.urllib3 self.BeautifulSoup self.celery self.cssutils self.Django self.django-celery self.django-crispy-forms self.django-paging self.django-picklefield self.django-social-auth self.django-static-compiler self.django-templatetag-sugar self.email-reply-parser self.gunicorn self.httpagentparser self.logan self.nydus self.Pygments self.pynliner self.python-dateutil self.python-memcached self.raven self.redis self.simplejson self.setproctitle self.South self.urllib3 self.BeautifulSoup self.celery self.cssutils self.Django self.django-celery self.django-crispy-forms self.django-paging self.django-picklefield self.django-social-auth self.django-static-compiler self.django-templatetag-sugar self.email-reply-parser self.gunicorn self.httpagentparser self.logan self.nydus self.Pygments self.pynliner self.python-dateutil self.python-memcached self.raven self.redis self.simplejson self.setproctitle self.South self.urllib3 self.nydus self.redis self.BeautifulSoup self.celery self.cssutils self.Django self.django-celery self.django-crispy-forms self.django-paging self.django-picklefield self.django-social-auth self.django-static-compiler self.django-templatetag-sugar self.email-reply-parser self.gunicorn self.httpagentparser self.logan self.nydus self.Pygments self.pynliner self.python-dateutil self.python-memcached self.raven self.redis self.simplejson self.setproctitle self.South self.urllib3];

  "setproctitle".meta.description = "A library to allow customization of the process title.";
  "setproctitle".meta.homepage = "http://code.google.com/p/py-setproctitle/";
  "setproctitle".meta.license = "BSD";
  "setproctitle".requires = [];

  "simplejson".meta.description = "Simple, fast, extensible JSON encoder/decoder for Python";
  "simplejson".meta.homepage = "http://github.com/simplejson/simplejson";
  "simplejson".meta.license = "MIT License";
  "simplejson".requires = [];

  "six".meta.description = "Python 2 and 3 compatibility utilities";
  "six".meta.homepage = "http://pypi.python.org/pypi/six/";
  "six".meta.license = "MIT";
  "six".requires = [];

  "urllib3".meta.description = "HTTP library with thread-safe connection pooling, file post, and more.";
  "urllib3".meta.homepage = "http://urllib3.readthedocs.org/";
  "urllib3".meta.license = "MIT";
  "urllib3".requires = [];

  "wsgiref".meta.description = "WSGI (PEP 333) Reference Library";
  "wsgiref".meta.homepage = "http://cheeseshop.python.org/pypi/wsgiref";
  "wsgiref".meta.license = "PSF or ZPL";
  "wsgiref".requires = [];

}
