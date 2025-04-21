# django-sysinfo

[![Pypi](https://badge.fury.io/py/django-sysinfo.svg)](https://badge.fury.io/py/django-sysinfo)
[![coverage](https://codecov.io/github/saxix/django-sysinfo/coverage.svg?branch=develop)](https://codecov.io/github/saxix/django-sysinfo?branch=develop)
[![Test](https://github.com/saxix/django-sysinfo/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-sysinfo/actions/workflows/test.yml)
[![Django](https://img.shields.io/pypi/frameworkversions/django/django-sysinfo)](https://pypi.org/project/django-sysinfo/)


Simple django app to expose system infos like libraries version, database server.

Easy to extend to add custom checks.

## Features


    - dump system informations
    - admin integration
    - API to add custom checks
    - simple echo
    - retrieve library version


## Quickstart

Install django-sysinfo::

    pip install django-sysinfo

put it in your `INSTALLED_APPS`::

    INSTALLED_APPS=[...
     'django_sysinfo'
    ]

add relevant entries in your url.conf::

    urlpatterns = (
        ....
        url(r'', include(django_sysinfo.urls)),
    )

or customize them::

    from django_sysinfo.views import http_basic_login, sysinfo

    urlpatterns = (
        url('sys/info/$', http_basic_login(sysinfo), name='sys-info'),
        url('sys/version/(?P<name>.*)/$', version, name='sys-version')
    )


Known issues and limitations
----------------------------

There are some limitations in the metrics returned by sysinfo, anyway this package is
not intended to be used as host/resources monitoring tool.

    - Disk space returns device info, any soft limits are ignored
    - Memory can be wrong in some virtual environments
