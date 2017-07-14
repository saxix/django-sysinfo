# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

here = os.path.dirname(__file__)
# sys.path.append(os.path.abspath(os.path.join(here, os.pardir)))
# sys.path.append(os.path.abspath(os.path.join(here, os.pardir, "demo")))

DEBUG = True
# TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "sysinfo",
        "HOST": "127.0.0.1",
        "PORT": "",
        "USER": "postgres",
        "PASSWORD": ""},
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:"},
}

TIME_ZONE = "Europe/Rome"
# LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(here, "media")
MEDIA_URL = ""
STATIC_ROOT = os.path.join(here, "static")


def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired "
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)


STATIC_URL = "/static/"
SECRET_KEY = "c73*n!y=)tziu^2)y*@5i2^)$8z$tx#b9*_r3i6o1ohxo%*2^a"

_mkdir(STATIC_ROOT)
_mkdir(MEDIA_ROOT)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
)
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]
ROOT_URLCONF = "demoproject.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django_sysinfo",
]
LOGIN_URL = "/admin/login/"
# TEMPLATE_LOADERS = (
#     "django.template.loaders.filesystem.Loader",
#     "django.template.loaders.app_directories.Loader",
# )

TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates",
     "DIRS": [
         # insert your TEMPLATE_DIRS here
     ],
     "APP_DIRS": True,
     "OPTIONS": {
         "debug": DEBUG,
         "context_processors": [
             # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
             # list if you haven"t customized them:
             "django.contrib.auth.context_processors.auth",
             "django.template.context_processors.debug",
             "django.template.context_processors.i18n",
             "django.template.context_processors.media",
             "django.template.context_processors.static",
             "django.template.context_processors.tz",
             "django.contrib.messages.context_processors.messages",
         ],
     },
     }
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "unique-snowflake"
    }
}

SYSINFO = {"host": True,
           "os": True,
           "python": True,
           "modules": True,
           "project": {
               "mail": True,
               "installed_apps": True,
               "databases": True,
               "MEDIA_ROOT": True,
               "STATIC_ROOT": True,
               "CACHES": True
           },
           "checks": None,
           "extra": None
           }

# ENABLE_SELENIUM = True
#
# DATE_FORMAT = "d-m-Y"
# TIME_FORMAT = "H:i"
# DATETIME_FORMAT = "d-m-Y H:i"
# YEAR_MONTH_FORMAT = "F Y"
# MONTH_DAY_FORMAT = "F j"
# SHORT_DATE_FORMAT = "m/d/Y"
# SHORT_DATETIME_FORMAT = "m/d/Y P"
# FIRST_DAY_OF_WEEK = 1
#
