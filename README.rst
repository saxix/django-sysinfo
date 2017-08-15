==============
django-sysinfo
==============

.. image:: https://badge.fury.io/py/django-sysinfo.png
    :target: https://badge.fury.io/py/django-sysinfo

.. image:: https://travis-ci.org/saxix/django-sysinfo.png?branch=master
    :target: https://travis-ci.org/saxix/django-sysinfo

Simple django app to expose system infos like libraries version, database server.

Easy to extend to add custom checks.

Features
--------

    - dump system informations
    - check API to add custom checks
    - simple echo
    - retrieve library version


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

.. |master-cov| image:: https://codecov.io/github/saxix/django-sysinfo/coverage.svg?branch=master
            :target: https://codecov.io/github/saxix/django-sysinfo?branch=master


.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-sysinfo.png?branch=develop
                  :target: http://travis-ci.org/saxix/django-sysinfo/

.. |dev-cov| image:: https://codecov.io/github/saxix/django-sysinfo/coverage.svg?branch=develop
        :target: https://codecov.io/github/saxix/django-sysinfo?branch=develop

