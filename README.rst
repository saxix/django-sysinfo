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

In our environment we manage dozens of Django applications and sometimes we need to answer questions like:

    - which application is using this broken/outdated package ?
    - which application is using that database ?


scan all the installed sites, is tedious, we have a documentation site with
all these infos, but we want to keep it always updated.
Here where django-sysinfo comes to help.


It provides a simple view that returns a json response containing:

- environment:
    - installed modules and version

- project:
    - MEDIA_ROOT/STATIC_ROOT path and available disk space
    - django installed apps
    - process path
    - temp dir path
    - databases:
        - ip
        - engine
        - version
    - mail server

- os:
    - name

- python:
    - version
    - executable path

- host:
    - cpu(s) number
    - free/total memory
    - NIC list and relative IP addresses

- extra:
    <user defined functions>


You can add entries and/or remove what can be dangerous in your enviroment.
The url is protected with Basic Authentication without install `RemoteUserBackend`.

Allowed user can be restricted using ``settings.SYSINFO_USERS``
 if not exists any superuser can use the endpoint::

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


Known issues and limitations
----------------------------

There are some limitations in the metrics returned by sysinfo, anyway this package is
not intended to be used as host/resources monitoring tool.

    - Disk space returns device info, any soft limits are ignored
    - Memory can be wrong in some virtual environments


Links
~~~~~

+--------------------+----------------+--------------+------------------------+
| Stable             | |master-build| | |master-cov| |                        |
+--------------------+----------------+--------------+------------------------+
| Development        | |dev-build|    | |dev-cov|    |                        |
+--------------------+----------------+--------------+------------------------+
| Project home page: |https://github.com/saxix/django-sysinfo                 |
+--------------------+---------------+----------------------------------------+
| Issue tracker:     |https://github.com/saxix/django-sysinfo/issues?sort     |
+--------------------+---------------+----------------------------------------+
| Download:          |http://pypi.python.org/pypi/django-sysinfo/             |
+--------------------+---------------+----------------------------------------+
| Documentation:     |https://django-sysinfo.readthedocs.org/en/latest/       |
+--------------------+---------------+--------------+-------------------------+

.. |master-build| image:: https://secure.travis-ci.org/saxix/django-sysinfo.png?branch=master
                    :target: http://travis-ci.org/saxix/django-sysinfo/

.. |master-cov| image:: https://coveralls.io/repos/saxix/django-sysinfo/badge.svg?branch=master&service=github
            :target: https://coveralls.io/github/saxix/django-sysinfo?branch=master


.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-sysinfo.png?branch=develop
                  :target: http://travis-ci.org/saxix/django-sysinfo/

.. |dev-cov| image:: https://coveralls.io/repos/saxix/django-sysinfo/badge.svg?branch=develop&service=github
        :target: https://coveralls.io/github/saxix/django-sysinfo?branch=develop

