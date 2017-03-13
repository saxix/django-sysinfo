=============
Configuration
=============

Configure
=========

.. code-block:: javascript

    SYSINFO = {"host": True,
           "os": True,
           "python": True,
           "modules": True,
           "project": True,
           "project.installed_apps": True,
           "project.MEDIA_ROOT": True,
           "project.STATIC_ROOT": True,
           "project.CACHES": True,
           "extra": None
           }

Sections
========

Host
----

.. code-block:: javascript

  "host": {
    "hostname": "host1",
    "fqdn": "host1.org",
    "cpus": 4,
    "network": {
      "en0": [
        "192.168.1.100/255.255.255.0"
      ],
      "lo0": [
        "127.0.0.1/255.0.0.0",
        "192.168.66.66/None"
      ]
    },
    "memory": {
      "percent": "74.5 bytes",
      "used": "5.0 GB",
      "available": "2.0 GB",
      "free": "64.0 MB",
      "total": "8.0 GB"
    }
  }

OS
--

.. code-block:: javascript

  "os": {
    "uname": [
      "Darwin",
      "host1.local",
      "16.4.0",
      "Darwin Kernel Version 16.4.0: Thu Dec 22 22:53:21 PST 2016; root:xnu-3789.41.3~3/RELEASE_X86_64",
      "x86_64"
    ],
    "name": "posix"
  },

Python
------

.. code-block:: javascript

  "python": {
    "executable": "/data/VENV/si/bin/python",
    "version": "2.7.13",
    "platform": "darwin",
    "info": "2.7.13 (default, Mar 10 2017, 12:55:49) \n[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)]",
    "maxunicode": [
      65535,
      "WARN"
    ]
  },


Modules
-------

.. code-block:: javascript

     "modules": {"alabaster": "0.7.7",
                  "apipkg": "1.4",
                  "django": "1.9.1",
                  "pytest": "2.8.5",
                  "xlwt-future": "0.8.0"},

Project
-------

.. code-block:: python

  "project": {
    "current_dir": "/data/PROJECTS/django-sysinfo",
    "tempdir": "/var/folders/vy/jjqmc4bj38z2rj90qzhwsczw0000gn/T",
  },

installed_apps
~~~~~~~~~~~~~~

.. code-block:: javascript

    "installed_apps": [
      [
        "django_sysinfo",
        "0.4a20160403211457"
      ]
    ]


MEDIA_ROOT
~~~~~~~~~~

.. code-block:: javascript

    "MEDIA_ROOT": {
      "path": "/data/PROJECTS/django-sysinfo/tests/demo/demoproject/media",
      "disk": {
        "used": "288.0 GB",
        "free": "176.0 GB",
        "total": "464.0 GB"
      }
    },

STATIC_ROOT
~~~~~~~~~~~

.. code-block:: javascript

    "STATIC_ROOT": {
      "path": "/data/PROJECTS/django-sysinfo/tests/demo/demoproject/static",
      "disk": {
        "used": "288.0 GB",
        "free": "176.0 GB",
        "total": "464.0 GB"
      }
    },

CACHES
~~~~~~

.. code-block:: javascript

    "CACHES": {
      "default": {
        "LOCATION": "unique-snowflake",
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
      }
    },


Databases
---------

.. code-block:: python

    "databases": {"default": {"engine": "django.db.backends.postgresql_psycopg2",
                                 "host": "127.0.0.1:",
                                 "name": "sysinfo",
                                 "server": "PostgreSQL 9.4.3 on x86_64-apple-darwin14.3.0, compiled by Apple LLVM version 6.1.0 (clang-602.0.53) (based on LLVM 3.6.0svn), 64-bit",
                                 "timezone": "UTC",
                                 "version": "9.4.3"},
                    "sqlite": {"engine": "django.db.backends.sqlite3",
                                "host": ":",
                                "name": ":memory:",
                                "server": "3.8.10.2",
                                "timezone": "UTC",
                                "version": "3.8.10.2"}},


EXTRA
-----

