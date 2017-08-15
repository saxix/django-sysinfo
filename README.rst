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


Sample output
-------------

    ::

    {
    "host": {
        "hostname": "jeeg-3.local",
        "fqdn": "jeeg-3.local",
        "cpus": 4,
        "network": {
            "lo0": [
                "127.0.0.1/255.0.0.0"
            ],
            "en0": [
                "192.168.0.101/255.255.255.0"
            ]
        },
        "memory": {
            "total": "8.0 GB",
            "available": "2.3 GB",
            "percent": "71.1 bytes",
            "used": "6.3 GB",
            "free": "117.1 MB"
        }
    },
    "os": {
        "uname": [
            "Darwin",
            "jeeg-3.local",
            "16.7.0",
            "Darwin Kernel Version 16.7.0: Thu Jun 15 17:36:27 PDT 2017; root:xnu-3789.70.16~2/RELEASE_X86_64",
            "x86_64"
            ],
        "name": "posix"
    },
    "python": {
        "executable": "/data/VENV/mercury/bin/python",
        "version": "3.6.0",
        "platform": "darwin",
        "info": "3.6.0 (default, Mar 28 2017, 09:03:14) \n[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)]",
        "maxunicode": [
            1114111,
            "OK"
        ]
        "modules": {
            "admin-extra-urls": "1.5",
            "alabaster": "0.7.10",
            "amqp": "2.2.1",
            "appnope": "0.1.0",
            "argh": "0.26.2",
            },
    },
    "project": {
        "current_dir": "/data/PROGETTI/saxix/mercury",
        "tempdir": "/var/folders/vy/jjqmc4bj38z2rj90qzhwsczw0000gn/T",
        "MEDIA_ROOT": {
            "path": "",
            "disk": {
                "total": "464.8 GB",
                "used": "458.4 GB",
                "free": "6.1 GB"
            }
        },
        "STATIC_ROOT": {
            "path": "/data/PROGETTI/saxix/mercury/src/mercury/web/static",
            "disk": {
                "total": "464.8 GB",
                "used": "458.4 GB",
                "free": "6.1 GB"
            }
        },
        "CACHES": {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:7777/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient"
                }
            },
            "lock": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:7777/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient"
                }
            }
        },
        "installed_apps": [
                [ "admin", "django.contrib.admin"],
                [
                "admin_extra_urls", "admin_extra_urls"],
                ["auth", "django.contrib.auth"],
                ["constance", "constance"],
            ],
        "mail": {
            "backend": "django.core.mail.backends.smtp.EmailBackend",
            "host": "smtp.gmail.com:587",
            "tls": false,
            "ssl": false,
            "status": "SMTP AUTH extension not supported by server."
            }
        }
    }

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

