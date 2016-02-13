# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os
import psutil
import socket
import sys
import tempfile
from collections import OrderedDict
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


def _get_database_infos(conn):
    engine = conn.settings_dict.get('ENGINE')
    ret = OrderedDict()
    if engine == 'django.db.backends.postgresql_psycopg2':
        import psycopg2.extensions

        ret['version'] = _run_database_statement(conn, 'SHOW server_version;')
        ret['encoding'] = _run_database_statement(conn, 'SHOW SERVER_ENCODING;')
        ret['collate'] = _run_database_statement(conn, 'SHOW LC_COLLATE;')
        ret['ctype'] = _run_database_statement(conn, 'SHOW LC_CTYPE;')
        isolation_level = conn.isolation_level
        for attr in ['ISOLATION_LEVEL_AUTOCOMMIT',
                     'ISOLATION_LEVEL_READ_UNCOMMITTED',
                     'ISOLATION_LEVEL_READ_COMMITTED',
                     'ISOLATION_LEVEL_REPEATABLE_READ',
                     'ISOLATION_LEVEL_SERIALIZABLE']:
            if conn.isolation_level == getattr(psycopg2.extensions, attr, None):
                isolation_level = attr

        ret['isolation_level'] = isolation_level
        ret['timezone'] = conn.connection.get_parameter_status('TimeZone')
        ret['info'] = _run_database_statement(conn, 'SELECT version();')

    elif engine == 'django.db.backends.sqlite3':
        ret['version'] = _run_database_statement(conn, 'select sqlite_version();')
    elif engine == 'django.db.backends.oracle':
        ret['version'] = _run_database_statement(conn, 'select * from v$version;')
    return ret


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


def get_databases(**kwargs):
    databases = OrderedDict()
    for alias in connections:
        conn = connections[alias]
        db = OrderedDict()
        db['engine'] = conn.settings_dict.get('ENGINE')
        db['host'] = '%(HOST)s:%(PORT)s' % conn.settings_dict
        db['name'] = conn.settings_dict.get('NAME')
        db.update(_get_database_infos(conn))
        databases[alias] = db
    return databases


def get_modules(**kwargs):
    modules = OrderedDict()
    for i in sorted(pip.get_installed_distributions(local_only=True),
                    key=lambda i: i.project_name.lower()):
        modules[i.project_name.lower()] = i.version
    return modules


def get_host(**kwargs):
    mem = psutil.virtual_memory()
    nic = psutil.net_if_addrs()
    host = OrderedDict()
    host['hostname'] = socket.gethostname()
    host['fqdn'] = socket.getfqdn()
    host['cpus'] = psutil.cpu_count()
    host['network'] = [[card, [d.address for d in data]] for card, data in nic.items()]

    host['memory'] = {'total': humanize_bytes(mem.total),
                      'available': humanize_bytes(mem.available),
                      'percent': humanize_bytes(mem.percent),
                      'used': humanize_bytes(mem.used),
                      'free': humanize_bytes(mem.free)}
    return host


def get_python(**kwargs):
    p = OrderedDict()
    p['executable'] = sys.executable
    p['version'] = "{0.major}.{0.minor}.{0.micro}".format(sys.version_info)
    p['platform'] = sys.platform
    p['info'] = sys.version
    p['maxunicode'] = (sys.maxunicode,
                       {True: 'OK', False: 'WARN'}[sys.maxunicode > 0xffff])
    return p


def get_device_info(path):
    info = psutil.disk_usage(os.path.realpath(path))
    return {'total': humanize_bytes(info.total),
            'used': humanize_bytes(info.used),
            'free': humanize_bytes(info.free)}


def get_caches_info():
    ret = dict(settings.CACHES)
    for k, v in ret.items():
        backend = settings.CACHES[k]['BACKEND']
        loc = settings.CACHES[k].get('LOCATION', None)
        if backend == 'django.core.cache.backends.filebased.FileBasedCache':
            ret[k]['status'] = get_device_info(loc)
    return ret


def get_project(**kwargs):
    project = OrderedDict()
    project['current_dir'] = os.path.realpath(os.curdir)
    project['tempdir'] = tempfile.gettempdir()
    project['MEDIA_ROOT'] = OrderedDict([('path', settings.MEDIA_ROOT),
                                         ('disk', get_device_info(settings.MEDIA_ROOT))])

    project['STATIC_ROOT'] = OrderedDict([('path', settings.STATIC_ROOT),
                                          ('disk', get_device_info(settings.STATIC_ROOT))])

    project['CACHES'] = get_caches_info()

    if config.installed_apps:
        project['installed_apps'] = get_istalled_apps()
    return project


def get_os(**kwargs):
    return {'uname': os.uname(),
            'name': os.name}


handlers = OrderedDict([('host', get_host),
                        ('os', get_os),
                        ('python', get_python),
                        ('modules', get_modules),
                        ('project', get_project),
                        ('databases', get_databases)])
valid_sections = handlers.keys()


def get_sysinfo(request):
    data = OrderedDict()
    sections = request.GET.get('s', None)
    if sections is None:
        sections = valid_sections
    else:
        sections = sections.split(',')

    for section in sections:
        if section in valid_sections and getattr(config, section):
            data[section] = handlers[section](config=config)

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
