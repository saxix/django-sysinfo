==============
django-sysinfo
==============

.. image:: https://badge.fury.io/py/django-sysinfo.png
    :target: https://badge.fury.io/py/django-sysinfo

.. image:: https://travis-ci.org/saxix/django-sysinfo.png?branch=master
    :target: https://travis-ci.org/saxix/django-sysinfo

Simple django app to expose system infos like libraries version, database server...

Rationale
---------

In our environment we manage dozens Django's applications and sometimes we need to answer questions like:

    - which application is using this broken/outdated package ?
    - which application is using that database ?
    ...

scan all the installed sites, is tedious, we have a documentation site with
all these infos, but we want to keep it always updated.
Here where django-sysinfo comes to help.


It provides a simple view that returns a json response containing:

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


You can add entries and/or remove what can be dangerous in your enviroment.
The url is protected with Basic Authentication without install `RemoteUserBackend`.

Allowed user to use the service can be restricted using ``settings.SYSINFO_USERS``
 if not exist any superuser can use the endpoint::

    settings.SYSINFO_USERS = ['username',]


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

