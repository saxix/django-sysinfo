# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os
import psutil
import sys
import tempfile
from pkg_resources import get_distribution

import pip
from django.conf import settings
from django.db import connections

from django_sysinfo.compat import get_istalled_apps

from .conf import config

UNKNOWN = 'unknown'


def _run_database_statement(conn, stm):
    if not stm:
        return UNKNOWN
    c = conn.cursor()
    c.execute(stm)
    row = c.fetchone()
    return row[0]


def get_database_version(conn):
    engine = conn.settings_dict.get('ENGINE')
    stmt = None

    if engine == 'django.db.backends.postgresql_psycopg2':
        stmt = 'SHOW server_version'
    elif engine == 'django.db.backends.sqlite3':
        stmt = 'select sqlite_version();'
    elif engine == 'django.db.backends.oracle':
        stmt = 'select * from v$version;'

    return _run_database_statement(conn, stmt)


def get_database_info(conn):
    engine = conn.settings_dict.get('ENGINE')
    stmt = None

    if engine == 'django.db.backends.postgresql_psycopg2':
        stmt = 'SELECT version();'
    elif engine == 'django.db.backends.sqlite3':
        stmt = 'select sqlite_version();'
    elif engine == 'django.db.backends.oracle':
        stmt = 'select * from v$version;'
    return _run_database_statement(conn, stmt)


def humanize_bytes(bytes, raw=False, precision=1):
    """Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    if raw:
        return bytes
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


def get_databases():
    databases = {}
    for alias in connections:
        conn = connections[alias]
        db = {'engine': conn.settings_dict.get('ENGINE'),
              'host': '%(HOST)s:%(PORT)s' % conn.settings_dict,
              # 'timezone': conn.timezone_name,
              'name': conn.settings_dict.get('NAME'),
              'version': get_database_version(conn),
              'server': get_database_info(conn)
              }
        databases[alias] = db
    return databases


def get_modules():
    modules = {}
    for i in pip.get_installed_distributions(local_only=True):
        modules[i.project_name.lower()] = i.version
    return modules


def get_host():
    mem = psutil.virtual_memory()
    nic = psutil.net_if_addrs()
    return {
        'cpus': psutil.cpu_count(),
        'network': [[card, [d.address for d in data]] for card, data in nic.items()],
        'memory': {'total': humanize_bytes(mem.total),
                   'available': humanize_bytes(mem.available),
                   'percent': humanize_bytes(mem.percent),
                   'used': humanize_bytes(mem.used),
                   'free': humanize_bytes(mem.free)},
    }


def get_python():
    return {'version': "{0.major}.{0.minor}.{0.micro}".format(sys.version_info),
            'info': sys.version,
            'executable': sys.executable,
            'platform': sys.platform}


def get_project(config):
    media = psutil.disk_usage(os.path.realpath(settings.MEDIA_ROOT))
    static = psutil.disk_usage(os.path.realpath(settings.STATIC_ROOT))
    project = {'current_dir': os.path.realpath(os.curdir),
               'tempdir': tempfile.gettempdir(),
               'MEDIA_ROOT': {'path': settings.MEDIA_ROOT,
                              'disk': {
                                  'total': humanize_bytes(media.total),
                                  'used': humanize_bytes(media.used),
                                  'free': humanize_bytes(static.free)},
                              },
               'STATIC_ROOT': {'location': settings.STATIC_ROOT,
                               'disk': {
                                   'total': humanize_bytes(static.total),
                                   'used': humanize_bytes(static.used),
                                   'free': humanize_bytes(static.free)},
                               },
               }
    if config.installed_apps:
        project['installed_apps'] = get_istalled_apps()
    return project


def get_sysinfo(request):
    data = {}
    if config.databases:
        data['databases'] = get_databases()

    if config.modules:
        data['modules'] = get_modules()

    if config.os:
        data['os'] = {'uname': os.uname(),
                      'name': os.name,
                      }

    if config.project:
        data['project'] = get_project(config)

    if config.host:
        data['host'] = get_host()

    if config.python:
        data['python'] = get_python()

    if config.extra:
        extras = {}
        for k, v in config.extra.items():
            extras[k] = v(request)
        data['extras'] = extras

    return data


def get_version(name):
    try:
        version = get_distribution(name).version
    except:
        version = UNKNOWN
    return version
