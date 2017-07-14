import logging
import warnings

import pytest

levelNames = {
    logging.CRITICAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "NOTSET",
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def pytest_addoption(parser):
    parser.addoption("--log", default=None, action="store",
                     dest="log_level",
                     help="enable console log")

    parser.addoption("--log-add", default="", action="store",
                     dest="log_add",
                     help="add package to log")


def pytest_configure(config):
    warnings.simplefilter("once", DeprecationWarning)

    if config.option.log_level:
        import logging
        level = config.option.log_level.upper()
        assert level in levelNames.keys()
        format = "%(levelname)-7s %(name)-30s %(funcName)-20s:%(lineno)3s %(message)s"
        formatter = logging.Formatter(format)

        handler = logging.StreamHandler()
        handler.setLevel(levelNames[level])
        handler.setFormatter(formatter)

        for app in ["test", "demoproject", "django_sysinfo"]:
            l = logging.getLogger(app)
            l.setLevel(levelNames[level])
            l.addHandler(handler)

        if config.option.log_add:
            for pkg in config.option.log_add.split(","):
                l = logging.getLogger(pkg)
                l.setLevel(levelNames[level])
                l.addHandler(handler)


# @pytest.fixture(autouse=True)
# def add_np(doctest_namespace):
#     import mock
#     doctest_namespace['mock'] = mock

@pytest.fixture
def cache(settings):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "unique-snowflake"
        },
        "a": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "127.0.0.1:11211",
        },
        "b": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "unix:/tmp/memcached.sock",
        },
        "c": {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "LOCATION": "/tmp/memcached.sock",
        },
        "d": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "my_cache_table",
        },
        "e": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/var/tmp/django_cache",
        },
        "f": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
    settings.CACHES = CACHES
