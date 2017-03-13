import pytest


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
