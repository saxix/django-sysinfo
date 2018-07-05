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

    parser.addoption("--docker", default=False, action="store_true",
                     help="start docker containers")


# @pytest.fixture(scope="module")
# def client():
#     import docker
#     return docker.from_env()
#
#
# @pytest.fixture(scope="module")
# def image(client):
#     client.images.build(path=, tag=NAME, rm=True)
#     yield client
#     client.images.remove(NAME)
#
#
# @pytest.fixture(scope="module", autouse=True)
# def container(client):
#
#     c = client.containers.run("mysql:5.7",
#                               remove=True,
#                               detach=True)
#     # FIXME: remove me (print)
#     print(111, 4444, c)
#     yield c
#     c.stop()


@pytest.fixture(scope="session", autouse=True)
def mysql(request):
    if request.config.option.docker:
        import docker
        client = docker.from_env()
        c = client.containers.run("mysql:8",
                                  ports={"3306": "3306"},
                                  remove=True,
                                  detach=True)
    yield
    if request.config.option.docker:
        c.stop()


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
            logger = logging.getLogger(app)
            logger.setLevel(levelNames[level])
            logger.addHandler(handler)

        if config.option.log_add:
            for pkg in config.option.log_add.split(","):
                logger = logging.getLogger(pkg)
                logger.setLevel(levelNames[level])
                logger.addHandler(handler)


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
