=============================
django-sysinfo
=============================

.. image:: https://badge.fury.io/py/django-sysinfo.png
    :target: https://badge.fury.io/py/django-sysinfo

.. image:: https://travis-ci.org/saxix/django-sysinfo.png?branch=master
    :target: https://travis-ci.org/saxix/django-sysinfo

Simple django app to expose system infos like libraries version, database server...

It provides a simple api and a view that returns a json response containing:

- database:
    - ip
    - engine
    - version

- environment:
    - installed modules and version

- project:
    - MEDIA_ROOT/STATIC_ROOT path and available disk space
    - django installed apps
    - process path
    - temp dir path

- os:
    - name

- python:
    - version
    - executable path

- host:
    - cpu(s) number
    - free/total memory
    - NIC list and relative IP addresses



a command line utility `django-sysinfo` can be used to remotely retrieve infos.


Documentation
-------------

The full documentation is at https://django-sysinfo.readthedocs.org.

Quickstart
----------

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

