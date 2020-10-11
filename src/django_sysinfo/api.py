# -*- coding: utf-8 -*-
import logging
import os
import psutil
import socket
import sys
import tempfile
from collections import OrderedDict

from django.views.debug import SafeExceptionReporterFilter
from pkg_resources import get_distribution

from django.conf import settings
from django.db import connections
from django.utils.module_loading import import_string

import six

from django_sysinfo.compat import get_installed_apps, get_installed_distributions
from django_sysinfo.utils import get_network, humanize_bytes

from .conf import config

logger = logging.getLogger(__name__)

UNKNOWN = "unknown"

if hasattr(SafeExceptionReporterFilter, 'cleanse_setting'):
    cleanse_setting = SafeExceptionReporterFilter().cleanse_setting
else:
    def cleanse_setting(key, value):
        from django.views.debug import HIDDEN_SETTINGS, CLEANSED_SUBSTITUTE
        if HIDDEN_SETTINGS.search(key):
            return CLEANSED_SUBSTITUTE
        return value


def _run_database_statement(conn, stm, offset=0):
    if not stm:
        return UNKNOWN
    c = conn.cursor()
    c.execute(stm)
    row = c.fetchone()
    if row:
        return row[offset]


def _get_database_infos(conn):
    engine = conn.settings_dict.get("ENGINE")
    ret = OrderedDict()
    if engine == "django.db.backends.mysql":
        ret["version"] = _run_database_statement(conn, "SELECT VERSION();")
        ret["user"] = _run_database_statement(conn, "SELECT USER();")
        # ret["basedir"] = _run_database_statement(conn, "SHOW VARIABLES LIKE '%BASEDIR%';", 1)
        # ret["max_connections"] = _run_database_statement(conn, "SHOW VARIABLES LIKE '%MAX_CONNECTIONS%';", 1)
    elif engine == "django.db.backends.postgresql_psycopg2":
        import psycopg2.extensions

        ret["version"] = _run_database_statement(conn, "SHOW server_version;")
        ret["encoding"] = _run_database_statement(conn, "SHOW SERVER_ENCODING;")
        ret["collate"] = _run_database_statement(conn, "SHOW LC_COLLATE;")
        ret["ctype"] = _run_database_statement(conn, "SHOW LC_CTYPE;")
        isolation_level = conn.isolation_level
        for attr in ["ISOLATION_LEVEL_AUTOCOMMIT",
                     "ISOLATION_LEVEL_READ_UNCOMMITTED",
                     "ISOLATION_LEVEL_READ_COMMITTED",
                     "ISOLATION_LEVEL_REPEATABLE_READ",
                     "ISOLATION_LEVEL_SERIALIZABLE"]:
            if conn.isolation_level == getattr(psycopg2.extensions, attr, None):
                isolation_level = attr

        ret["isolation_level"] = isolation_level
        ret["timezone"] = conn.connection.get_parameter_status("TimeZone")
        ret["info"] = _run_database_statement(conn, "SELECT version();")

    elif engine == "django.db.backends.sqlite3":
        ret["version"] = _run_database_statement(conn, "select sqlite_version();")
    elif engine == "django.db.backends.oracle":
        ret["version"] = _run_database_statement(conn, "select * from $version;")
    else:
        ret["info"] = 'DATABASE NOT SUPPORTED'
    return ret


def get_databases(**kwargs):
    databases = OrderedDict()
    for alias in connections:
        db = OrderedDict()
        try:
            conn = connections[alias]
            db["engine"] = conn.settings_dict.get("ENGINE")
            db["host"] = "%(HOST)s:%(PORT)s" % conn.settings_dict
            db["name"] = conn.settings_dict.get("NAME")
            db.update(_get_database_infos(conn))
        except Exception as e:
            db["error"] = str(e)
        finally:
            databases[alias] = db
    return databases


def get_modules(**kwargs):
    modules = OrderedDict()
    for i in sorted(get_installed_distributions(),
                    key=lambda i: i.project_name.lower()):
        modules[i.project_name.lower()] = i.version
    return modules


def get_host(**kwargs):
    mem = psutil.virtual_memory()
    host = OrderedDict()
    host["hostname"] = socket.gethostname()
    host["fqdn"] = socket.getfqdn()
    host["cpus"] = psutil.cpu_count()
    host["network"] = get_network()

    host["memory"] = {"total": humanize_bytes(mem.total),
                      "available": humanize_bytes(mem.available),
                      "percent": humanize_bytes(mem.percent),
                      "used": humanize_bytes(mem.used),
                      "free": humanize_bytes(mem.free)}
    return host


def get_python(**kwargs):
    p = OrderedDict()
    p["executable"] = sys.executable
    p["version"] = "{0.major}.{0.minor}.{0.micro}".format(sys.version_info)
    p["platform"] = sys.platform
    p["info"] = sys.version
    p["maxunicode"] = (sys.maxunicode,
                       {True: "OK", False: "WARN"}[sys.maxunicode > 0xffff])
    return p


def get_mail(**kwargs):
    def check():
        from django.core.mail import get_connection
        try:
            conn = get_connection(fail_silently=False)
            conn.open()
            ret = "OK"
            conn.close()
        except Exception as e:
            ret = str(e)
        return ret

    p = OrderedDict()
    p["backend"] = settings.EMAIL_BACKEND
    p["host"] = "{0}:{1}".format(settings.EMAIL_HOST, settings.EMAIL_PORT)
    p["tls"] = getattr(settings, "USE_TLS", False)
    p["ssl"] = getattr(settings, "USE_SSL", False)
    p["status"] = check()
    return p


def get_device_info(path):
    try:
        info = psutil.disk_usage(os.path.realpath(path))
        return {"total": humanize_bytes(info.total),
                "used": humanize_bytes(info.used),
                "free": humanize_bytes(info.free)}
    except OSError as e:
        return {"ERROR": str(e)}


def get_caches_info():
    ret = dict(settings.CACHES)
    for k, v in ret.items():
        backend = settings.CACHES[k]["BACKEND"]
        loc = settings.CACHES[k].get("LOCATION", None)
        if backend == "django.core.cache.backends.filebased.FileBasedCache":
            ret[k]["status"] = get_device_info(loc)
    return ret


def get_project(**kwargs):
    project = OrderedDict()
    project["current_dir"] = os.path.realpath(os.curdir)
    project["tempdir"] = tempfile.gettempdir()

    if config.MEDIA_ROOT:
        project["MEDIA_ROOT"] = OrderedDict([("path", settings.MEDIA_ROOT),
                                             ("disk", get_device_info(settings.MEDIA_ROOT))])

    if config.STATIC_ROOT:
        project["STATIC_ROOT"] = OrderedDict([("path", settings.STATIC_ROOT),
                                              ("disk", get_device_info(settings.STATIC_ROOT))])

    if config.DATABASES:
        project["DATABASES"] = get_databases()

    if config.CACHES:
        project["CACHES"] = get_caches_info()

    if config.installed_apps:
        project["installed_apps"] = get_installed_apps()

    if config.mail:
        project["mail"] = get_mail(**kwargs)
    return project


def get_os(**kwargs):
    return {"uname": os.uname(),
            "name": os.name}


def run_check(id, request=None, fail_silently=True, fail_status=500):
    status = 200
    try:
        v = config.checks[id]
        if isinstance(v, six.string_types):
            c = import_string(v)
            ret, status = c(request)
        elif callable(v):
            ret, status = v(request)
        else:
            ret = v
    except Exception as e:
        ret = "ERROR"
        status = fail_status
        logger.exception(e)
        if settings.DEBUG:
            ret = str(e)
        if not fail_silently:
            raise

    return ret, status


def get_checks(request=None):
    checks = {}
    if config.checks:
        for k, v in config.checks.items():
            checks[k] = run_check(k)

    return checks


def get_extra(config, request=None):
    extras = {}
    for k, v in config.extra.items():
        try:
            if isinstance(v, six.string_types):
                c = import_string(v)
                extras[k] = c(request)
            elif callable(v):
                extras[k] = v(request)
            else:
                extras[k] = v
        except Exception as e:
            logger.exception(e)
            if settings.DEBUG:
                extras[k] = str(e)
    return extras


def get_environment(**kwargs):
    ret = {}
    for key, value in os.environ.items():
        ret[key] = cleanse_setting(key, value)
    return ret


handlers = OrderedDict([("host", get_host),
                        ("os", get_os),
                        ("environ", get_environment),
                        ("python", get_python),
                        ("modules", get_modules),
                        ("project", get_project),
                        ("extra", get_extra),
                        ("checks", get_checks)])

valid_sections = handlers.keys()


def get_sysinfo(request):
    data = OrderedDict()
    sections = request.GET.get("s", None)
    if sections is None:
        sections = valid_sections
    else:
        sections = sections.split(",")

    for section in sections:
        if section in valid_sections and getattr(config, section):
            data[section] = handlers[section](config=config, request=request)

    return data


def get_version(name):
    try:
        version = get_distribution(name).version
    except Exception:
        version = UNKNOWN
    return version
